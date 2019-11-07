from enum import Enum

"""
File containing states represented as enums
"""


class State(Enum):
    """
    States for the FSM
    Examples of states may be found on page 16
    """
    INIT, READ, VERIFY_READ, VERIFY_PWCHANGE, ACTIVE, SET_PW, LED, TIME, LOGOUT = range(
        9)
