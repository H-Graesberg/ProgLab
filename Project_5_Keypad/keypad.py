"""
File containing the representation of the physical keypad
"""
import sys
import time
import RPi.GPIO as GPIO



class Keypad:
    """
    Class representing the physical keypad
    """

    def __init__(self):
        '''Constructor'''
        # These are suggested by the exercise (4.1, p 10)
        self.keypad_row_pins = (18, 23, 24, 25)
        self.keypad_column_pins = (17, 27, 22)

        self.pin_dictionary = self.construct_pin_dictionary()
        # Setup:
        self.setup()

    def setup(self):
        """
        Set up the Led board properties; see 4.2.1 p11
        :return:
        """
        # We should use BCM according to the exercise
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Set up row pins as output:
        for rp in self.keypad_row_pins:
            GPIO.setup(rp, GPIO.OUT)

        # Set up column pins as input:
        for cp in self.keypad_column_pins:
            GPIO.setup(cp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def do_polling(self):
        """
        Does a continuous polling of the keypad until it finds a pressed button
        :return: Row and column pins of the button pressed
        """
        # Do polling in an infinite loop

        while True:
            # Iterate through all row pins
            for rp in self.keypad_row_pins:
                # Set each row pin to high sequentially
                GPIO.output(rp, GPIO.HIGH)
                # print(rp)

                # Check each column pin
                for cp in self.keypad_column_pins:
                    count = 0
                    while GPIO.input(cp) == GPIO.HIGH:
                        count += 1
                        time.sleep(0.01)
                        if count > 20:
                            return (rp, cp)
                    # print(cp)
                    # If this is high we found the combination of row and index pressed
                    # if GPIO.input(cp) == GPIO.HIGH:
                    #    print(rp, cp)
                    #    return (rp, cp)
                # Reset output from current row pin
                GPIO.output(rp, GPIO.LOW)

    def get_next_signal(self):
        """
        Do polling to check which row and column is being pressed.
        Then find out which value this represents, and return this
        :return: Symbol pressed on the keypad
        """
        # Check which row and column is pressed
        #pressed_combination = self.do_polling()
        # Return the value pressed on the keypad
        return self.pin_dictionary[self.do_polling()]

    def construct_pin_dictionary(self):
        """
        Help function for constructing a dictionary
        :return: Dictionary: K: [row_pin, column_pin] -> V: Any
        """

        # All symbols on the keypad
        symbols = (1, 2, 3,
                   4, 5, 6,
                   7, 8, 9,
                   "*", 0, "#")

        # Adding to this
        pin_dictionary = {}

        # Save an index to know which symbol to add
        i = 0
        # Iterate through each pin
        for row in self.keypad_row_pins:
            for column in self.keypad_column_pins:
                # Update dictionary
                pin_dictionary[(row, column)] = symbols[i]
                i += 1
        # print(pin_dictionary)
        return pin_dictionary


def main():
    '''Main_func test'''
    keypad = Keypad()
    keypad.setup()
    print("hello")

    try:
        sig = -1
        while sig != 2:
            print(keypad.get_next_signal())

    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
    GPIO.cleanup()


if __name__ == '__main__':
    main()
