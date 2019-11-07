import Project_3.crypto_utils as crypto_util
import random


class Cypher:
    """superclass for all encryption/decryption algorithms"""

    def __init__(self):
        """Constructs necessary constants"""
        self.crypt_alph = [chr(i) for i in range(32, 127)]
        # self.crypt_alph_string = "".join(self.crypt_alph)
        self.length_alph = 95
        self.start_alph = 32
        self.end_alph = 127

    def encode(self, text, key):
        """Crypts the text with the given key"""
        pass

    def decode(self, text, key):
        """Decrypts the text with given key"""
        pass

    def verify(self, non_crypt, key):
        """Encrypts and decrypts the same text, and verifies if it is the same"""
        if self.decode(self.encode(non_crypt, key), key) == non_crypt:
            return True
        return False

    def generate_keys(self):
        """Generates keys for given algorithm"""
        pass


class Caesar(Cypher):
    """Encryption by adding given number to ascii-value"""

    def encode(self, text, key):
        """Encodes the text with given key by addition"""
        bitrep = crypto_util.blocks_from_text(text, 1)
        coded = []
        for element in bitrep:
            element = (element + key) % self.end_alph
            if element < self.start_alph:
                element += self.start_alph
            coded.append(element)
        return crypto_util.text_from_blocks(coded, 1)

    def decode(self, text, key):
        """Decodes the given text with given key"""
        key = self.end_alph - key
        return self.encode(text, key)

    def generate_keys(self):
        """Generate a random key"""
        return self.crypt_alph[random.randint(1, self.length_alph)]


class Multiplication(Cypher):
    """Use to multiplicate with a number to decrypt/encrypt"""

    def encode(self, text, key):
        """Encodes the text with given key by multiplication"""
        bitrep = crypto_util.blocks_from_text(text, 1)
        coded = []
        for element in bitrep:
            element = (element * key) % self.end_alph
            coded.append(element)
        return crypto_util.text_from_blocks(coded, 1)

    def decode(self, text, key):
        """Decodes the given text with given key, must be same as encode, will find inverted key"""
        # print(key)
        new_key = crypto_util.modular_inverse(key, self.end_alph)
        # print(new_key)
        return self.encode(text, new_key)

    def generate_keys(self):  # Must be an easier method here, have one in Store
        """Generate a random key, something weird inside this... almost right"""
        possible_numbers = [1, 2, 3, 5, 6, 7, 10, 11, 15, 19, 20, 24, 41, 44, 53, 57,
                            62, 64, 66, 73, 82, 85, 92, 102, 106, 107, 111, 115, 116, 119,
                            120, 121, 123, 124, 125]
        return random.choice(possible_numbers)


class Affine(Cypher):
    """Decode/encode by combining Caesar and Multiplication"""

    def __init__(self):
        super().__init__()
        self.caesar = Caesar()
        self.multiplication = Multiplication()

    def encode(self, text, key):
        """Encodes the text with given key-tuple with combo of caesar and multi"""
        crypt1 = self.multiplication.encode(text, key[0])
        crypt2 = self.caesar.encode(crypt1, key[1])
        return crypt2

    def decode(self, text, key):
        """Decodes the given text with given key-tuple"""
        decrypt1 = self.caesar.decode(text, key[1])
        decrypt2 = self.multiplication.decode(decrypt1, key[0])
        return decrypt2

    def generate_keys(self):
        """Generates key-tuple"""
        rand_key_tuple = (
            self.multiplication.generate_keys(),
            self.caesar.generate_keys())
        return rand_key_tuple


class Unbreakable(Cypher):
    """Uses a word for encryption and decryption"""

    def encode(self, text, key: str):
        """Encodes text with a word as key"""
        crypto = ""
        for i in range(len(text)):
            crypto += key[i % len(key)]
        text_as_numbers = crypto_util.blocks_from_text(text, 1)
        crypto_key_numbers = crypto_util.blocks_from_text(crypto, 1)
        crypted_text = []
        for i in range(len(text_as_numbers)):
            add = (text_as_numbers[i] + crypto_key_numbers[i]) % self.end_alph
            if add < self.start_alph:
                add += self.start_alph
            crypted_text.append(add)
        return crypto_util.text_from_blocks(crypted_text, 1)

    def decode(self, text, key):
        """Decodes text with key, finds the inverted word first"""
        decode_key = crypto_util.blocks_from_text(key, 1)
        for i in range(len(decode_key)):
            decode_key[i] = self.end_alph - decode_key[i] % self.end_alph
        decryptkey = crypto_util.text_from_blocks(decode_key, 1)
        return self.encode(text, decryptkey)


class RSA(Cypher):
    """Unhackable encryption-algorithm with some public keys"""

    def encode(self, text, key):
        """Encodes the text with key wich is generated by another RSA"""
        text_as_numbers = crypto_util.blocks_from_text(text, 1)
        new_block = []
        for block in text_as_numbers:
            new_block.append(pow(block, key[1], key[0]))
        return new_block

    def decode(self, text, key):
        """Decodes the text with key synchronized with encryptor"""
        decrypted_list = [pow(integer, key[1], key[0]) for integer in text]
        return crypto_util.text_from_blocks(decrypted_list, 1)

    def generate_keys(self):
        """Generates one common key, one decryptionkey(prime) and one encryptionkey(prime)"""
        p, q = 0, 0
        check_keys = -1
        while p == q or check_keys != 1:
            p = crypto_util.generate_random_prime(8)
            q = crypto_util.generate_random_prime(8)
            phi = (p - 1) * (q - 1)
            encode_key = random.randint(3, phi - 1)
            check_keys = check_prev_remainder(encode_key, phi)
        n = p * q
        decode_key = crypto_util.modular_inverse(encode_key, phi)
        self.key = (n, decode_key)
        return (n, encode_key)


def check_prev_remainder(_a, _b):
    """returns the greatest common divisor"""
    previous_remainder, remainder = _a, _b
    current_x, previous_x, current_y, previous_y = 0, 1, 1, 0
    while remainder > 0:
        previous_remainder, (quotient, remainder) = remainder, divmod(
            previous_remainder, remainder)
        current_x, previous_x = previous_x - quotient * current_x, current_x
        current_y, previous_y = previous_y - quotient * current_y, current_y
    return previous_remainder


class Person:
    """Superclass for all persons that is involved with cryptography"""

    def __init__(self, key, cypher_alg):
        """Constructor, sets a key for encrypt/decrypt and type of crypt-algorithm which is used"""
        self.key = key
        if isinstance(cypher_alg, Cypher):
            self.cypher_alg = cypher_alg

    def set_key(self, key):
        """Sets the cryptating-key"""
        self.key = key

    def get_key(self):
        """Returns the key used in encryption/decryption"""
        return self.key

    def operate_cipher(self, text):
        """Demands the subclasses must have this method"""
        pass


class Sender(Person):
    """Encodes a text"""

    def operate_cipher(self, text):
        """Encrypt the text"""
        return self.cypher_alg.encode(text, self.key)


class Reciever(Person):
    """Decodes a text"""

    def operate_cipher(self, text):
        """Decrypt the text"""
        return self.cypher_alg.decode(text, self.key)


class Hacker(Reciever):
    """Decodes encryption-algorithms with brute force"""

    def __init__(self, cypher_alg):
        """Have knowledge about the difference kind of algorithms"""
        super().__init__(None, cypher_alg)
        self.words = None
        self.caesar = Caesar()
        self.multiplication = Multiplication()
        self.affine = Affine()
        self.unbreak = Unbreakable()
        self.list_to_multi = [1, 2, 3, 5, 6, 7, 10, 11, 15, 19, 20, 24, 41, 44, 53, 57,
                              62, 64, 66, 73, 82, 85, 92, 102, 106, 107, 111, 115, 116, 119,
                              120, 121, 123, 124, 125]
        with open("english_words.txt", 'r') as word_file:
            self.words = {line.rstrip('\n') for line in word_file}

    def operate_cipher(self, text):
        """Decodes the crypted word by brute force"""
        matches = []
        if isinstance(self.cypher_alg, Caesar):
            for i in range(127):
                example = self.caesar.decode(text, i)
                if example in self.words:
                    matches.append(example)
            if len(matches) != 0:
                return matches
            return "no matches with caesar"
        if isinstance(self.cypher_alg, Multiplication):
            for element in self.list_to_multi:
                example = self.multiplication.decode(text, element)
                if example in self.words:
                    matches.append(example)
            if len(matches) != 0:
                return matches
            return "no matches with multi"
        if isinstance(self.cypher_alg, Affine):
            for i in range(127):
                for j in range(1, 127):
                    example = self.affine.decode(text, (j, i))
                    if example in self.words:
                        matches.append(example)
            if len(matches) != 0:
                return matches
            return "No matches with unbreakable"
        if isinstance(self.cypher_alg, Unbreakable):
            for word in self.words:
                decrypt_text = self.unbreak.decode(text, word)
                if decrypt_text in self.words:
                    matches.append(decrypt_text)
            if len(matches) != 0:
                return matches
            return "No matches with unbreakable"


def main():
    algo_caesar = Caesar()
    algo_multi = Multiplication()
    algo_affine = Affine()
    algo_unbreak = Unbreakable()

    algo_rsa1 = RSA()
    algo_rsa2 = RSA()
    algo_rsa1.key = algo_rsa2.generate_keys()
    print(algo_rsa1.key)
    print(algo_rsa2.key)
    print(algo_rsa1.encode("abc!~", algo_rsa1.key))
    test = algo_rsa1.encode("abc!~", algo_rsa1.key)
    print(algo_rsa2.decode(test, algo_rsa2.key))

    check = "textured"

    print(algo_caesar.verify("abcd", 5))
    print(algo_multi.verify("abcd", 15))
    print(algo_affine.verify("abcd!", (5, 2)))
    print(algo_unbreak.verify("abcdsdfa~", "tamr~"))
    print(algo_unbreak.verify(check, "wrong"))

    hidden_word = algo_caesar.encode(check, 4)
    hack_caesar = Hacker(algo_caesar)
    print(hack_caesar.operate_cipher(hidden_word))

    hidden_word = algo_multi.encode(check, 2)
    hack_multi = Hacker(algo_multi)
    print(hack_multi.operate_cipher(hidden_word))

    hidden_word = algo_affine.encode(check, (5, 2))
    hack_affine = Hacker(algo_affine)
    print(hack_affine.operate_cipher(hidden_word))

    hidden_word = algo_unbreak.encode(check, "wrong")
    hack_unbreak = Hacker(algo_unbreak)
    print(hack_unbreak.operate_cipher(hidden_word))


main()
