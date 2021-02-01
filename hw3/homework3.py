from nltk import word_tokenize
from nltk import pos_tag
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.stem.porter import *
from collections import Counter
import numpy as np
import collections
import nltk
import sys
import re


def edit_distance(a, b):
    # Referenced: https://www.educative.io/edpresso/the-levenshtein-distance-algorithm
    row = len(a) + 1
    column = len(b) + 1
    dist = [[0 for i in range(column)] for j in range(row)]

    # Initialize first row of matrix
    for i in range(row):
        dist[i][0] = i

    # Initialize first column of matrix
    for j in range(column):
        dist[0][j] = j

    for i in range(1, row):
        for j in range(1, column):
            if a[i - 1] == b[j - 1]:
                count = 0
            else:
                count = 1

            # find min operation for the distance
            # insertion, deletion, and substitution
            dist[i][j] = min(dist[i][j - 1] + 1,
                             dist[i - 1][j] + 1,
                             dist[i - 1][j - 1] + count)

    print(dist[len(a)][len(b)])

def process_data(text):
    # lowercase all text
    text = text.lower()

    # use replace function - replace all "--" to " "
    text = text.replace("--", " ")

    # remove numbers and punctation, replace with ' ' with regex
    text = re.sub(r'[.?!,:;$#"@()=+%&\-\'\n\d]', ' ', text)

    return text


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please enter a filename for system arg")
        quit()

    # read file as plain text
    with open('moby_dick.txt', 'r') as f:
        raw_text = f.read()

        raw_text = process_data(raw_text)

        # tokenize text & print number of total tokens
        tokens = nltk.word_tokenize(raw_text)
        print("\nNumber of tokens:", len(tokens))

        # store tokenized text into a list
        tokens = [t for t in tokens if t]

        # get unique tokens
        unique_tokens = list(set(tokens))
        print("\nNumber of unique tokens:", len(unique_tokens))

        # remove stopwords
        stop_words = set(stopwords.words('english'))

        # create list of important words from unique token list
        important_words = [t for t in unique_tokens if not t in stop_words]
        print("\nNumber of important words:", len(important_words))

        # create list of tuples of the word and stemmed word
        stemmer = PorterStemmer()
        stemmed = [(t, stemmer.stem(t)) for t in important_words]

        # create a dictionary, key is the stem, value is list of words
        stem_dict = {}
        for word, stem in stemmed:
            stem_dict.setdefault(stem, []).append(word)
        print("Number of dictionary entries:", len(stem_dict))

        # for 25 dictionary entries with longest lists, print stem and list
        for k, v in sorted(stem_dict.items(), key=lambda item: len(item[1]), reverse=True)[:25]:
            print(k, v)

        print("The edit distance between continu, and continue:", edit_distance("continu", "continue"))
        print("The edit distance between continu, and continuously:", edit_distance("continu", "continuously"))
        print("The edit distance between continu, and continues:", edit_distance("continu", "continues"))
        print("The edit distance between continu, and continual:", edit_distance("continu", "continual"))
        print("The edit distance between continu, and continuing:", edit_distance("continu", "continuing"))
        print("The edit distance between continu, and continuation:", edit_distance("continu", "continuation"))
        print("The edit distance between continu, and continually:", edit_distance("continu", "continually"))
        print("The edit distance between continu, and continued:", edit_distance("continu", "continued"))

        # Step 11: POS tagging on original text from step 3
        tags = nltk.pos_tag(tokens)

        # creat POS dictionary, key is POS, value is number of words of the POS
        pos_dict = {}
        for token, pos in tags:
            if pos not in pos_dict:
                pos_dict[pos] = 1
            else:
                pos_dict[pos] += 1
        sorted_dict = sorted(pos_dict, key=pos_dict.get, reverse=True)
        for pos in sorted_dict:
            print(pos, ':', pos_dict[pos])
