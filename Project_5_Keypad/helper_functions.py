"""
This file contains some helper functions that may be used other places in the project
"""


def signal_is_digit(signal):
    '''True if digit'''
    return 48 <= ord(str(signal)) <= 57


def signal_is_digit_in_range(signal, min_digit, max_digit):
    '''digit in range'''
    if signal_is_digit(signal):
        return min_digit <= signal <= max_digit
    return False


def signal_is_digit_between_0_and_5(signal):
    '''digit between 0, 5'''
    return signal_is_digit_in_range(signal, 0, 5)


def any_signal(signal):
    '''If any signal'''
    return True
