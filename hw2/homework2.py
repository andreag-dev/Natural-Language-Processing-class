from nltk import word_tokenize
from nltk import pos_tag
from nltk import sent_tokenize
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
from collections import Counter
from random import seed
from random import randint
import random
import nltk
import sys
import re


def process_data(text):
    # reduce tokens to tokens that are alpha, not stopwords and length > 5
    text = [t for t in text if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]

    # lemmatize tokens and used set() to retrieve list of unique lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in text]
    unique_lemmas = list(set(lemmas))

    # pos tagging on unique lemmas, print out first 20 tagged items
    tags = nltk.pos_tag(unique_lemmas)
    print(tags[:20])

    # create list of unique lemmas nouns
    nouns = [token for token, pos in pos_tag(unique_lemmas) if pos.startswith('N')]

    # print number of tokens and nouns
    print("\nNumber of tokens: ", len(text))
    print("\nNumber of nouns: ", len(nouns))

    return tokens, nouns


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter a filename for system arg")
        quit()

    # read file as plain text
    with open('anat19.txt', 'r') as f:
        text = f.read()

        tokens = word_tokenize(text)

        # lowercase the text, remove punctuation and numbers
        tokens = [t.lower() for t in tokens if t.isalpha()]

        # calc lexical diversity(num of unique tokens / total tokens)
        print("Lexical diversity: %.2f" % (len(set(tokens)) / len(tokens)))
        # print(tokens)
        tokens, nouns = process_data(tokens)

        # create empty dictionary
        dict = {}
        for noun in nouns:
            dict[noun] = tokens.count(noun)
        # sort dictionary by the greatest values of occurrence, in descending order
        sorted_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        print(sorted_dict[:50])

        # Save 50 most common words and counts to a list
        common_words = []
        for word in sorted_dict:
            common_words.append(word[0])

        # user gets 5 points to start with
        score = 5
        end = 0
        seed(1234)

        print('\nLets play a word guessing game!')
        # randomly choose one of the 50 words from common_words list
        random_word = common_words[random.randint(0, len(common_words))]

        # add underscore for each letter in the random chosen word
        underscore = ['_'] * len(random_word)
        print('_' * len(random_word))

        game_finished = False
        while game_finished is False:
            # prompt user to enter a letter
            guess = input('Enter a letter:')

            if score == 0 or guess == '!':
                print("Out of points, game over.")
                break

            if guess in random_word:
                score = score + 1
                print("Right! Score is ", score)

                # loop through letters in the random word
                for i, letter in enumerate(random_word):
                    if letter != "_" and guess == letter:
                        # replace underscore with letter
                        underscore[i] = letter

                # print list of joined guessed letters
                print(''.join(underscore))

                # if all letters guessed end game and print score
                if "_" not in underscore:
                    game_finished = True
                    print("You solved it!")
                    print("Current score: ", score)
                else:
                    game_finished = False

            # if user enters wrong letter, -1 score
            else:
                score = score - 1
                print("Sorry, guess again. Score is ", score)

