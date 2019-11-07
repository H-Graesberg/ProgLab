from helper_functions import signal_is_digit
from keypad import Keypad
from ledboard import Ledboard


"""
Class for the KPC Agent which manages the system
"""

path_to_password_file = "password.txt"

total_leds = 6


class KPC:
    """
    KPC Agent which communicates with the keypad and Finite State Machine
    """

    def __init__(self, keypad, ledboard):
        self.keypad = keypad
        self.ledboard = ledboard

        self.override_signal = ""
        self.led_id = 0
        self.led_duration = 0

        self.password = ""
        self.password_old = ""

    def init_password_entry(self, symbol):
        """
        Resets password buffer and initialize a start up sequence
        :return:
        """
        self.reset_password_field(symbol)

        # Signal that Pi is awake
        self.ledboard.startup_show()  # Changed from twinkle to startup
        print("startupsequence, INIT")

    def reset_password_field(self, symbol):
        '''Resets the field'''
        self.password = ""
        print("reset_password_field")

    def add_signal_to_password_input(self, symbol):
        """
        Adds a symbol to the current password input
        :param symbol: Digit pressed on the keypad
        :return:
        """
        self.password += str(symbol)
        self.ledboard.light_led(1, 1)  # flash on pressed button
        print("adding_signal_to_password_input: ", symbol)

    def get_next_signal(self):
        """
        Return either the overload signal if present, or simply query the keypad
        :return: Next signal
        """
        if len(self.override_signal) > 0:
            # Should clear override signal here
            override_signal = self.override_signal
            self.override_signal = ""
            print("if get_next_signal: ", override_signal)
            return override_signal

        else:
            return self.keypad.get_next_signal()

    def verify_login(self, symbol):
        """
        Check input password and compare to correct password stored in text file.
        Store the result as override signal
        :return:
        """
        f = open(path_to_password_file, "r")
        correct_password = f.readline()
        f.close()
        print("current password: ", self.password)

        # Compare input password and password from file
        if self.password == correct_password:
            print("verify login: Y, Correct password!")
            self.override_signal = "Y"
            # Signal success to LEDs for 3 seconds
            self.twinkle_leds(3)

        else:
            print("verify login: N, Wrong password!")
            self.override_signal = "N"
            # Signal failure to LEDs for 3 seconds
            self.flash_leds(3)

    def verify_password_change(self, symbol):
        """
        Checks if new password is valid
        :return:
        """
        # Check if password has at least 4 digits
        valid = len(self.password) >= 4
        print("verify_password_change")

        if valid:
            # Check all characters in password and break if any are not valid
            for char in self.password:
                if not signal_is_digit(char):
                    valid = False
                    print("wrong format on password or to few digits")
                    break

        # Check if valid
        if valid:
            f = open(path_to_password_file, "w")
            f.write(self.password)
            f.close()
            print("verify_p_c: sucsess")
            # Signal success to LEDs for 3 seconds
            self.twinkle_leds(3)

        else:
            # Signal failure to LEDs for 3 seconds
            print("verify_p_c: failure")
            self.flash_leds(3)

    def set_led(self, symbol):
        """
        Set which LED to manipulate
        :param symbol:
        :return:
        """
        self.led_id = int(symbol)

    def add_duration_digit(self, symbol):
        """
        Add a digit for the LED light duration
        :param symbol:
        :return:
        """
        self.led_duration = self.led_duration + int(symbol)

    def activate_led(self, symbol):
        """
        Activates the set led (in led_id) for (led_duration) seconds
        :param symbol:
        :return:
        """

        self.ledboard.light_led(self.led_id, self.led_duration)
        # Reset led id and duration
        self.led_id, self.led_duration = 0, 0

    def power_down(self, symbol):
        """
        Called when the user logs out. Should do something to the LEDs
        :param symbol:
        :return:
        """
        self.ledboard.shutdown_show()

    def flash_leds(self, k):
        """
        Briefly flash all leds on the board.
        Called when the user inputs a wrong password
        Turns all LEDs for some time before turning them off again several times
        :param k: Time duration to flash the LEDs
        :return:
        """
        self.ledboard.flash_all_leds(k)

    def twinkle_leds(self, k):
        """
        Twinkles all lights by flashing leds in sequence
        Called when user input a correct password and successfully logs in
        Turns on and off all LEDs in sequence
        :param k:
        :return:
        """
        self.ledboard.twinkle_all_leds(k)

    def do_nothing(self, symbol):
        '''Does nothing'''
        return


def main():
    keypad = Keypad()
    ledboard = Ledboard()
    KPC(keypad, ledboard)


if __name__ == '__main__':
    main()
