
"""
File containing rules for the FSM
"""


class Rule:
    """
    Base rule class that all other rules should derive from
    """

    def __init__(self, state1, state2, signal, action):
        """
        Initializing each rule with the following arguments:
        :param state1: Triggering state
        :param state2: New state of the FSM when the rule fires
        :param signal: Triggering signal
        :param action: The action that the agent will be instructed to perform if this rule fires
        """

        self.state1 = state1
        self.state2 = state2
        self.signal = signal
        self.action = action
