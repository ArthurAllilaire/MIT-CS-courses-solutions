# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for char in secret_word:
      if char not in letters_guessed:
        return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    result = "'"
    for char in secret_word:
      if char not in letters_guessed:
        result += "_ "
      else:
        result += char
    result += "'"
    return result



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    result = string.ascii_lowercase
    for char in letters_guessed:
      result = result.replace(char, "")
    return result
      

def hangman(secret_word):
  '''
  secret_word: string, the secret word to guess.
  
  Starts up an interactive game of Hangman.
  
  * At the start of the game, let the user know how many 
    letters the secret_word contains and how many guesses s/he starts with.
    
  * The user should start with 6 guesses

  * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.
  
  * Ask the user to supply one guess per round. Remember to make
    sure that the user puts in a letter!
  
  * The user should receive feedback immediately after each guess 
    about whether their guess appears in the computer's word.

  * After each guess, you should display to the user the 
    partially guessed word so far.
  
  Follows the other limitations detailed in the problem write-up.
  '''
  # initialising variables
  letters_guessed = []
  guesses = 6
  warnings = 3
  dashed_line = "---------------"

  def new_round(guesses, letters_guessed = letters_guessed):
    """
    Needs to be called with nothing, there is default parameter of letters_guessed
    should be called at the start of every round and prints all that is necessary, returns None if input given is not valid, and returns valid input.
    """

    # print(get_guessed_word(secret_word, letters_guessed) )
    print("You have " + str(guesses) + " guesses left.")
    print("Available letters: " + get_available_letters(letters_guessed))
    ans = input("Please guess a letter: ")
    if ans.isalpha():
      return ans.lower()
    else:
      return None 
    
  # One off starting the game
  print("Welcome to the game Hangman!")
  print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
  print(get_guessed_word(secret_word, letters_guessed) )


  while is_word_guessed(secret_word, letters_guessed) != True and guesses > 0:
    valid = new_round(guesses)
    if valid != None:#If guess is a valid result, then do
      valid = valid.lower()
      letters_guessed.append(valid)  
      #check if the letter is in the word
      if valid in secret_word:
        print("Good guess!!  " + get_guessed_word(secret_word, letters_guessed))
      else:
        print("Oops! that letter is not in my word." + get_guessed_word(secret_word, letters_guessed))
        if valid in "aeiou":
          guesses -= 2
        else:
          guesses -= 1
    else: #consequences for not inputing right character
      print("Oops! That is not a valid letter.")
      warnings -= 1
      if warnings == 0:
        guesses -= 1
        print("You have one less guess as you have inputed the wrong thing 3 times, guesses: " + str(guesses))
        warnings = 3
      print("You have " + str(warnings) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))

    print(dashed_line)

  if is_word_guessed(secret_word, letters_guessed):
      print("Congratulations you won!")
      total_score = guesses * (26 - len(get_available_letters(letters_guessed)))
      print("Your total score for this game is: " + total_score)
  else:
    print("Sorry, you ran out of guesses. The word was " + secret_word)

     




# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    #initialising list
    letters_used = []
    # first of all, we shall compare the lengths of the two, removing from my_word any spaces using the strip() function. If the length is different return False.
    if len(my_word) != len(other_word):
      return False
    
    # Then for every instance of a character that is not a _ I would check to see that at the same place in the other word it matches. if not return false. also need to add the character to a list of characters, duplicates don't amtter, but would be better if were none
    # check first index, if _ skip, else look at same index in other word. If != return false, also put letter of my_word into list. Repeat till end of word.
    for i in range(len(my_word)):
      if my_word[i] == "_":
        pass
      elif my_word[i] != other_word[i]:
        return False
      else:
        letters_used.append(my_word[i])
    # make sure every place in other_word where _ in my_word doesn't have the same letter as those in list created in step above. If they do then return false.
    for i in range(len(my_word)):
      if my_word[i] != "_":
        pass
      elif other_word[i] in letters_used:
        return False
    # Once all passed return true
    return True

def show_possible_matches(my_word, wordlist = wordlist):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    #initialising variables
    matching_words = 0
    # Wordlist is a list of strings, so I think I can loop over them using for i in range(len(wordlist))
    print("Possible word matches are:")
    for i in range(len(wordlist)):
    # Callmatch with gaps to see if word at index could be my_word, IF it is it returns true and then add it to a list fo strings
      if match_with_gaps(my_word, str(wordlist[i])):
        print(wordlist[i], end = ' ')
        matching_words += 1
    if matching_words == 0:
      print("No matches found")
    print("")

    



def hangman_with_hints(secret_word):
  '''
  secret_word: string, the secret word to guess.
  
  Starts up an interactive game of Hangman.
  
  * At the start of the game, let the user know how many 
    letters the secret_word contains and how many guesses s/he starts with.
    
  * The user should start with 6 guesses
  
  * Before each round, you should display to the user how many guesses
    s/he has left and the letters that the user has not yet guessed.
  
  * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
    
  * The user should receive feedback immediately after each guess 
    about whether their guess appears in the computer's word.

  * After each guess, you should display to the user the 
    partially guessed word so far.
    
  * If the guess is the symbol *, print out all words in wordlist that
    matches the current guessed word. 
  
  Follows the other limitations detailed in the problem write-up.
  '''
  # initialising variables
  letters_guessed = []
  guesses = 6
  warnings = 3
  dashed_line = "---------------"

  # One off starting the game
  print("Welcome to the game Hangman!")
  print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
  print(get_guessed_word(secret_word, letters_guessed) )


  while is_word_guessed(secret_word, letters_guessed) != True and guesses > 0:
    my_word = get_guessed_word(secret_word, letters_guessed)
    letters_left = get_available_letters(letters_guessed)
    print("You have " + str(guesses) + " guesses left.")
    print("Available letters: " + letters_left)
    ans = input("Please guess a letter: ")
    if ans.isalpha():
      ans = ans.lower()
      letters_guessed.append(ans)  
      #check if the letter is in the WORDLIST_FILENAME
      if ans not in letters_left:
        print("You have already said that letter, try again." + my_word)
      elif ans in secret_word:
        print("Good guess!!  " + get_guessed_word(secret_word, letters_guessed))
      else:
        print("Oops! that letter is not in my word." + my_word)
        if ans in "aeiou":
          guesses -= 2
        else:
          guesses -= 1
    elif ans == "*":
      my_word = my_word.replace(" ","")
      my_word = my_word.replace("'","")
      show_possible_matches(my_word)
    else: #consequences for not inputing right character
      print("Oops! That is not a valid letter.")
      warnings -= 1
      if warnings == 0:
        guesses -= 1
        print("You have one less guess as you have inputed the wrong thing 3 times, guesses: " + str(guesses))
        warnings = 3
      print("You have " + str(warnings) + " warnings left: " + my_word)

    print(dashed_line)

  if is_word_guessed(secret_word, letters_guessed):
      print("Congratulations you won!")
      total_score = guesses * (26 - len(get_available_letters(letters_guessed)))
      print("Your total score for this game is: " + str(total_score))
  else:
    print("Sorry, you ran out of guesses. The word was " + secret_word)




# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
