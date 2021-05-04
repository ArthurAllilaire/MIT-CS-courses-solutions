print("You have " + guesses + " left.")
print("Available letters: " + get_available_letters(letters_guessed))
ans = input("Please guess a letter: ")
if ans.isalpha():
  letters_guessed.append(ans.lower())
else:
  warnings -= 1
  if warnings == 0:
    guesses -= 1
    print("You have one less guess as you have inputed the wrong thing 3 times, guesses: " + guesses)
    warnings = 3

  print("Oops! That is not a valid letter. You have " + warnings + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
ans = input("Please guess a letter: ")
valid = new_round()
