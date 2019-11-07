
import arduino_connect  # This is the key import so that you can access the serial port.

# Codes for the 5 signals sent to this level from the Arduino

_dot = 0
_dash = 1
_symbol_pause = 2
_word_pause = 3
_reset = 4


# Morse Code Class
class Morse_decoder():
    '''Takes input from arduino and converts the signals to symbols/words/sentences'''
    serial_port = ''
    current_symbol = ''
    current_word = ''

    _morse_codes = {'01': 'a', '1000': 'b', '1010': 'c', '100': 'd', '0': 'e', '0010': 'f', '110': 'g', '0000': 'h',
                    '00': 'i', '0111': 'j',
                    '101': 'k', '0100': 'l', '11': 'm', '10': 'n', '111': 'o', '0110': 'p', '1101': 'q', '010': 'r',
                    '000': 's', '1': 't',
                    '001': 'u', '0001': 'v', '011': 'w', '1001': 'x', '1011': 'y', '1100': 'z', '01111': '1',
                    '00111': '2', '00011': '3',
                    '00001': '4', '00000': '5', '10000': '6', '11000': '7', '11100': '8', '11110': '9', '11111': '0'}


    def __init__(self, sport=True):
        '''The constructor, connects to arduino'''
        if sport:
            self.serial_port = arduino_connect.pc_connect()
        self.reset()

    def reset(self):
        '''Resets all the instance-variables'''
        self.current_word = ''
        self.current_symbol = ''

    # This should receive an integer in range 0-4 from the Arduino via a serial port
    def read_one_signal(self, port=None):
        '''Returns the signal from arduino, between 0 and 4'''
        connection = port if port else self.serial_port
        while True:
            # Reads the input from the arduino serial connection
            data = connection.readline()
            if data:
                return data

    def decoding_loop(self):
        '''Starts the loop to detect input from arduino and process it to a integer'''
        while True:
            s = self.read_one_signal(self.serial_port)
            #print(s)
            #self.process_signal(int(chr(s[1])))
            for byte in s:
                self.process_signal(int(chr(byte))) ##Går igjennom s som er signalet. Litt uklart her hva den gjør med
                                                    ##Deler av signalet som ikke er tallverdi?

    def process_signal(self, signal):
        '''Checks the input and command what to do with the signal'''
        if (signal == 0) or (signal == 1):
            self.update_current_symbol(signal)
        elif signal == 2:
            self.handle_symbol_end()
        elif signal == 3:
            self.handle_word_end()
        elif signal == 4:       #exit the program
            exit()

    def update_current_symbol(self, signal):
        '''Adds 0 or 1 to the current symbol'''
        if signal == 0:
            self.current_symbol += '0'
        else:
            self.current_symbol += '1'

    def handle_symbol_end(self):
        '''Checks up the symbol in morse_codes and update the current word with this letter/number
        Also clears current symbol'''
        real_symbol = self._morse_codes.get(self.current_symbol)
        if (real_symbol == None):
            real_symbol = 'å'   #just in case the symbol does not exist
        #print(real_symbol)  #See each letter
        self.update_current_word(real_symbol)
        self.current_symbol = ''

    def update_current_word(self, symbol):
        '''adds a letter/number (or å if value = none) to current word'''
        self.current_word += symbol
        #print(self.current_word)   #See word for each new letter



    def handle_word_end(self):
        '''prints out the word and clears the variable to make it ready for more symbols'''
        self.handle_symbol_end()
        real_word = self.current_word
        self.current_word = ''
        if (real_word == ''):
            print('No word')
        else:
            print(real_word) #Will not work when end='' in cmd, why?

def run():
    '''Makes it more efficent in cmd. Error when launching in pyCharm, why?'''
    m = Morse_decoder()
    m.decoding_loop()

run()


''' To test if this is working, do this in python command window:

> from morse_skeleton import *

'''
