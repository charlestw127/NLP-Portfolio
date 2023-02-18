#Charles Wallis
#CTW170000
#2/18/2023

import sys   
import os    
import re    
import pickle
import random
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 

#open file from a data folder within the same folder as the python file
def readFile(filepath):
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    return text_in

#print number tags of list
def printNum(tags_list, num):
    count = 0
    for t in tags_list: 
        print(t)
        count += 1 
        if count == num:
            break
    return

#process data into tokens and noun lemmas
def processData(data):
    data = data.lower() #make word lowercase
    text_tokens = word_tokenize(data) #tokenize the word
    text_tokens = [t for t in text_tokens if t.isalpha() and t not in stopwords.words('english')]
    text_tokens = [t for t in text_tokens if len(t) >= 5] #remove alpha, stopword, and <5 length tokens
    
    wnl = WordNetLemmatizer()
    text_lemmas = [wnl.lemmatize(t) for t in text_tokens] #lemmatize token
    unique_text_lemmas = list(set(text_lemmas)) #set of unique lemma
    text_tags = nltk.pos_tag(unique_text_lemmas) #tag pos on unique lemma
    
    printNum(text_tags, 20) #print the first 20 tagged items
    noun_lemmas = [ t for t in text_tags if t[1] == 'NN' or t[1] == 'NNS' or t[1] == 'NNP'] #list of noun lemma
    print("Number of initial tokens: ", len(text_tokens)) #print token length
    print("Number of nouns: ", len(noun_lemmas)) #print noun length
    return text_tokens, noun_lemmas

#remove a random noun from the dictionary list and return it
def chooseWord(nouns):
    word = random.choice(nouns)
    nouns.remove(word)
    return word, nouns

#Running the actual game
def game(nouns):
    #game instruction
    print("\n===========================Word Guessing Game===========================")
    print(" A random noun is selected, and each letter will be shown as underscores")
    print(" You will start off with 5 points, and you die if your score goes negative")
    print(" If you guess a correct letter, +1 point, and the letters are shown")
    print(" If you guess an incorrect letter, -1 point")
    print(" Enter '!' as your guess to quit")

    points = 5
    cur_char = '.' #current character 
    cur_word = ""  #current word
    cur_word_progress = ""
    guessed_letters = []
    guessed_words = [] #list of guessed words
    word_found = True
    #play round while points is not negative, and user doesn't enter '!'
    while points > 0 and not cur_char == "!":
        #if word_found, reset the round
        if word_found:
            word_found = False #reset bool
            guessed_letters = [] #reset guessed
            cur_word_progress = "" #reset progress
            if len(nouns) < 1: #check noun list
                print("You've guessed all the words!")
                break
            #choose a word from list and remove it from the list
            cur_word, nouns = chooseWord(nouns)
            for i in cur_word:
                cur_word_progress += "_" #underscores for words
        print(cur_word_progress) #print the underscores
        cur_char = input("\nPlease input a letter to guess: ")

        #if input is !
        if cur_char == '!':
            print("\n===========Game Over===========")
            print("The word was: ", cur_word)
            print("Score: ", points)
            print("Word Count: ", len(guessed_words))
            print("Words: ", guessed_words)
            #reset guessed letter list
            guessed_letters = []
            break

        #make sure input isalpha
        if not cur_char.isalpha():
            print("Entered: " + cur_char + " which is not a letter or a '!', please try again.")
            continue
        #if correct guess
        if cur_char in cur_word and cur_char not in guessed_letters:
            #fill letter and +1 point
            for i in range(len(cur_word)):
                if cur_char == cur_word[i]:
                    cur_word_progress = cur_word_progress[:i] + cur_char + cur_word_progress[i+1:]
            points += 1
            print("Correct, 1 point added")
            print("Current Points: ", points)
            guessed_words.append(cur_char)
        #if wrong guess
        elif cur_char not in guessed_letters: 
            points -= 1
            print("Your guess was not in the word, 1 point lost")
            print("Current Points: ", points)
            guessed_letters.append(cur_char)

        # If score negative end game
        if points < 0:
            print("\n===========Game Over===========")
            print("You reached negative score")
            print("The word was: ", cur_word)
            print("Score: ", points)
            print("Word Count: ", len(guessed_words))
            print("Words: ", guessed_words)
            break
    # Reset the values
    points = 5
    cur_char = '.'
    cur_word_progress = ""
    guessed_letters = []
    guessed_words = []
    word_found = True
    return

#main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Specify the parameter to be data/anat19.txt')
    else:
        filePath = sys.argv[1] #set path to anat19.txt
        fileData = readFile(filePath) #read anat19.txt

    #process text data to tokenize and get lemmas
    text_tokens, noun_lemmas = processData(fileData)
    #calculate lexical diversity
    print("\nLexical Diversity: %.2f" % (len(noun_lemmas) / len(text_tokens)))

    #create a sorted dictionary of words by count order
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in text_tokens]
    counts = {t:lemmas.count(t) for t in noun_lemmas}
    sorted_count = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    #print the list of top 50 most commmon words
    print("\n50 most common words:")
    common_list = []
    for i in range(50):
        print(sorted_count[i][0][0])
        common_list.append(sorted_count[i][0][0])
    
    #play the game
    game(common_list)
