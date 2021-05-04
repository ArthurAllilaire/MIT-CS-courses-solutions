# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'ps4-words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        valid_words = self.valid_words[:]
        return valid_words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        result = {}
        lowercase_letters = string.ascii_lowercase
        for i in lowercase_letters:
            index = lowercase_letters.index(i) + shift
            if index >= 26:
                index = index - 26 
            result[i] = lowercase_letters[index]
        uppercase_letters = string.ascii_uppercase
        for i in uppercase_letters:
            index = uppercase_letters.index(i) + shift
            if index >= 26:
                index = index - 26 
            result[i] = uppercase_letters[index]
        return result
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        dictionary = Message.build_shift_dict(self, shift)
        text = Message.get_message_text(self)
        result = ""
        letters = string.ascii_letters
        for i in text:
            if i in letters:
                new_letter = dictionary[i]
                result += new_letter
            else:
                result += i
        return result

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self,shift)
        self.message_text_encrypted = Message.apply_shift(self,shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        PlaintextMessage(Message.get_message_text(self), shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        # Create number_of_english_words counter = 0
        number_of_english_words = 0
        # Create decrypeted variable
        final_decrypted_message = ""
        # create shift value
        final_shift_value = 0
        # for all possible s values (loop from 0 to 26)
        for s in range(26):
            #counter for number of english words
            counter = 0
        # convert the encrypted message into a decrypted message
            decrypted_message = Message.apply_shift(self, 26-s)
        # split it into a list
            message_words = decrypted_message.split(" ")
        # loop over the list
            for i in message_words:
        #for every word in the list that is a word add 1 to a counter
                if is_word(Message.get_valid_words(self), i):
                    counter += 1
        # if the counter is greater than number_of_english_words replace it and change the shift value to corresponding s value
            if counter > number_of_english_words:
                number_of_english_words = counter
                final_decrypted_message = decrypted_message
                final_shift_value = 26-s
        return (final_shift_value,final_decrypted_message)

if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #first test case(PlaintextMessage)
    plaintext = PlaintextMessage('sense', 10)
    print('Expected Output: coxco')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    #first test case (CiphertextMessage)
    ciphertext = CiphertextMessage('coxco')
    print('Expected Output:', (16, 'sense'))
    print('Actual Output:', ciphertext.decrypt_message())

    #Second test case
    plaintext = PlaintextMessage('Life is good', 4)
    print('Expected Output: Pmji mw kssh')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    #Second test case (CiphertextMessage)
    ciphertext = CiphertextMessage('Pmji mw kssh')
    print('Expected Output:', (22, 'Life is good'))
    print('Actual Output:', ciphertext.decrypt_message())
    # TODO: best shift value and unencrypted story 
    cipherstory = CiphertextMessage(get_story_string())
    print(cipherstory.decrypt_message())
    
    
