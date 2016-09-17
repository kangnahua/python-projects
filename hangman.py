# Hangman game

import random
import string

WORDLIST_FILENAME = "hangman.txt"

def loadWords():
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

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    n = 0
    for letter in lettersGuessed:
        if letter in secretWord:
            n += 1
    if n == len(secretWord):
        return True
    return False


def getGuessedWord(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    '''
    guessedWord = secretWord
    for let in guessedWord:
        if let not in lettersGuessed:
            guessedWord = guessedWord.replace(let, '_ ')
    return guessedWord



def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    availableLetters = string.ascii_lowercase
    for letter in lettersGuessed:
        if letter in availableLetters:
            availableLetters = availableLetters.replace(letter, '')
    return availableLetters
    

def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game, Hangman!")
    
    wordList = loadWords()
    secretWord = chooseWord(wordList)
    print("I am thinking of a word that is %i letters long." % len(secretWord))
    print('-' * 13)
    
    lettersGuessed = []
    life = 8
    
    while life >= 1 and not isWordGuessed(secretWord, lettersGuessed):
        availableLetters = getAvailableLetters(lettersGuessed)
        
        print("You have {} guesses left.".format(life))
        print("Available letters: ", end='')
        print(getAvailableLetters(lettersGuessed))
        
        guess = input("Please guess a letter: ").lower()
        
        if (guess not in secretWord) and (guess not in lettersGuessed):
            lettersGuessed.append(guess)
            print("Oops! That letter is not in my word: ", end='')
            print(getGuessedWord(secretWord, lettersGuessed))
            life -= 1
        elif (guess not in secretWord) and (guess in lettersGuessed):
            print("Oops! You've already guessed that letter: ",end='')
            print(getGuessedWord(secretWord, lettersGuessed))
        elif (guess in secretWord) and (guess in lettersGuessed):
            print("Oops! You've already guessed that letter: ", end='')
            print(getGuessedWord(secretWord, lettersGuessed))
        elif (guess in secretWord) and (guess not in lettersGuessed):
            lettersGuessed.append(guess)
            print("Good guess: ", end='')
            print(getGuessedWord(secretWord, lettersGuessed))
        
        print('-' * 12)
    
    if isWordGuessed(secretWord, lettersGuessed):
        print("Congratulations, you won!")
    else:
        print("Sorry, you ran out of guesses. The word was {}.".format(secretWord))

if __name__ == "__main__":
    secretWord = chooseWord(wordlist).lower()
    hangman(secretWord)
