from inspect import isfunction
import states
from helper_functions import any_signal, signal_is_digit, signal_is_digit_between_0_and_5
from keypad import Keypad
from kpc import KPC
from ledboard import Ledboard
from rules import Rule


"""
Primary file containing the Finite State Machine class
"""

fsm_states = states.State
number_of_leds = 6


class FSM:
    """
    Finite State Machine class
    """

    def __init__(self):
        self.rules = []
        self.state = fsm_states.INIT
        self.signal = None

        # Components:
        self.keypad = Keypad()
        self.ledboard = Ledboard()
        self.kpc = KPC(self.keypad, self.ledboard)

        # Setting up rules:
        # Init:
        self.add_rule(
            Rule(
                fsm_states.INIT,
                fsm_states.READ,
                any_signal,
                self.kpc.init_password_entry))

        # Read:
        # On digits, simply add it to password
        self.add_rule(
            Rule(
                fsm_states.READ,
                fsm_states.READ,
                signal_is_digit,
                self.kpc.add_signal_to_password_input))

        # On *, password is complete. Verify and write a overload signal to
        # memory
        self.add_rule(
            Rule(
                fsm_states.READ,
                fsm_states.VERIFY_READ,
                "*",
                self.kpc.verify_login))
        # Else return to init
        self.add_rule(
            Rule(
                fsm_states.READ,
                fsm_states.INIT,
                any_signal,
                self.kpc.reset_password_field))

        # Verify:
        # Verify password by getting a Y signal from the agent. Might change
        # action later?
        self.add_rule(
            Rule(
                fsm_states.VERIFY_READ,
                fsm_states.ACTIVE,
                "Y",
                self.kpc.do_nothing))
        # ELse return to read
        self.add_rule(
            Rule(
                fsm_states.VERIFY_READ,
                fsm_states.INIT,
                any_signal,
                self.kpc.reset_password_field))
        # TODO Er det ikke tilbake til init her? Er jo feil passord...

        # From Active to 1) SET_PW, 2) LED, 3) LOGOUT:
        change_password_button = 9
        # On ^this button, change state to set_pw
        self.add_rule(
            Rule(
                fsm_states.ACTIVE,
                fsm_states.SET_PW,
                change_password_button,
                self.kpc.init_password_entry))
        # On a digit between 0 and 5, change state to LED and save which LED
        # that has been chosen
        self.add_rule(
            Rule(
                fsm_states.ACTIVE,
                fsm_states.LED,
                signal_is_digit_between_0_and_5,
                self.kpc.set_led))
        # On "#", change state to logout
        self.add_rule(
            Rule(
                fsm_states.ACTIVE,
                fsm_states.LOGOUT,
                "#",
                self.kpc.do_nothing))

        # 1) SET_PW:
        # On digit, add this to password        //TODO: HVORFOR TO HER?
        self.add_rule(
            Rule(
                fsm_states.SET_PW,
                fsm_states.SET_PW,
                signal_is_digit,
                self.kpc.add_signal_to_password_input))
        self.add_rule(
            Rule(
                fsm_states.SET_PW,
                fsm_states.SET_PW,
                signal_is_digit,
                self.kpc.add_signal_to_password_input))
        # On *, check if password is valid and write to memory if it is
        self.add_rule(
            Rule(
                fsm_states.SET_PW,
                fsm_states.VERIFY_PWCHANGE,
                "*",
                self.kpc.verify_password_change))
        # Else, return to active    TODO: AGAIN STRANGE WITH THE ELSE-SENTENCE,
        # FROM METHOD IN KPC?
        self.add_rule(
            Rule(
                fsm_states.VERIFY_PWCHANGE,
                fsm_states.ACTIVE,
                any_signal,
                self.kpc.do_nothing))

        # 2) LED:   TODO: ISNT LINE 74 UNNECESSARY, IS THE SAME IN LINE 59? BETTER WITH ADD_DURATION_DIGIT
        # On a digit between 0 and 5, change state to LED and save which LED
        # that has been chosen
        self.add_rule(
            Rule(
                fsm_states.LED,
                fsm_states.LED,
                signal_is_digit_between_0_and_5,
                self.kpc.set_led))
        # On *, confirm LED TODO: MOST BE ADD_DURATION_DIGIT(SYMBOL) ON 74
        self.add_rule(
            Rule(
                fsm_states.LED,
                fsm_states.TIME,
                "*",
                self.kpc.do_nothing))

        # Time: TODO: JUST KIDDING, HERE IS TIME... BUT WHY THE DOUBLE UP OF SET_LED?
        # On digit, add that value to duration
        self.add_rule(
            Rule(
                fsm_states.TIME,
                fsm_states.TIME,
                signal_is_digit,
                self.kpc.add_duration_digit))
        # On *, activate the chosen LED for the chosen amount of seconds
        self.add_rule(
            Rule(
                fsm_states.TIME,
                fsm_states.ACTIVE,
                "*",
                self.kpc.activate_led))

        # Logout
        # On # logout completely and return to init phase
        self.add_rule(
            Rule(
                fsm_states.LOGOUT,
                fsm_states.INIT,
                "#",
                self.kpc.power_down))  # CHANGED TO SHUTDOWN_FLASH HERE
        # Else, return to active TODO WHEN DOES THIS HAPPEN?
        self.add_rule(
            Rule(
                fsm_states.LOGOUT,
                fsm_states.LOGOUT,
                any_signal,
                self.kpc.do_nothing))

        # TODO: THINK I THOGHT OF RULES AS A LOOP... BUT NOT NECESARRY
        # APPENDING THINGS TWICE?

    def add_rule(self, rule):
        """
        Adds a rule to the FSM's list of rules
        :param rule:
        :return:
        """
        self.rules.append(rule)

    def get_next_signal(self):
        """
        Querys the agent for the next signal to use
        :return:
        """
        self.signal = self.kpc.get_next_signal(
        )  # This isnt in the code?? why requires a symbol...

    def run_rules(self):
        """
        Iterates through all rules and apply each until we have a match.
        When this happens, fire that rule and return
        :return:
        """
        for rule in self.rules:
            if self.apply_rule(rule):
                self.fire_rule(rule)
                return

    def apply_rule(self, rule):
        """
        Apply a rule by checking if it is equal to the signal or accepts the signal as input
        :param rule:
        :return: Boolean representing if the rule matches the current signal
        """
        # Check is signal is a function
        if self.state == rule.state1:
            if isfunction(rule.signal):
                # Return matching function on signal
                return rule.signal(self.signal)
            else:
                # Return simple comparison between symbol and signal
                return self.signal == rule.signal
        return False

        # TODO CHECK FOR STATE HERE=?

    def fire_rule(self, rule):
        """
        Fires a rule by changing state and executing the rule's action
        :param rule:
        :return:
        """
        # Set next state
        self.state = rule.state2
        # Fire action with signal as the relevant symbol
        rule.action(self.signal)
        # TODO THIS ONE FIRES RIGHT ACTION? TWO ARGS, SELF.AGENT?
        # added two args instead of just signal, to many args

    def main_loop(self):
        """
        Main loop of the FSM
        :return:
        """
        # Do until FSM is in finale state
        # TODO SOMETHING STRANGE WITH THIS LOOP-THING...
        # TODO DOES IT ENSURE IT IS IN THE RIGHT RULES?
        # okay, changes the state to read but not the rule...
        while True:
            # Fetch next signal
            self.get_next_signal()
            print(self.state)
            print(self.signal)
            print("current password: ", self.kpc.password, "\n")
            # Run rule checking
            self.run_rules()


def main():
    print("oppdatert.")
    fsm = FSM()
    fsm.main_loop()


if __name__ == '__main__':
    main()
