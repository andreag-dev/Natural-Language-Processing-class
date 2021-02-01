from nltk.util import ngrams
from nltk import word_tokenize
from nltk.corpus import stopwords
import sys
import pickle
import nltk
import math


# referenced and modified compute_prob function from github
def compute_prob(text, unigram_dict, bigram_dict, V):
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))
    p = 1  # calculate p using Laplace smoothing

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0

        p = p * ((n + 1) / (d + V))

    return p

if __name__ == '__main__':
    # open pickle file and read in pickled dictionaries
    with open('dictionaries1.pickle', 'rb') as handle:

        uni_dict1, bi_dict1, uni_dict2, bi_dict2, uni_dict3, bi_dict3 = pickle.load(handle)

        # uni_dict1, bi_dict1 = English
        # uni_dict2, bi_dict2 = Italian
        # uni_dict3, bi_dict3 = French

    output = open("output_file1.txt", "w")

    with open("LangId.test", 'r') as f:
        for line in f:
            test = f.readline()
            # add length of the 3 unigram dictionaries
            V = len(uni_dict1) + len(uni_dict2) + len(uni_dict3)

            # calculate probability
            english_prob = compute_prob(test, uni_dict1, bi_dict1, V)
            italian_prob = compute_prob(test, uni_dict2, bi_dict2, V)
            french_prob = compute_prob(test, uni_dict3, bi_dict3, V)

            # find max probability
            if italian_prob > english_prob:
                output.write("Italian\n")
            else:
                output.write("English\n")
            if french_prob > english_prob:
                output.write("French\n")
                if italian_prob > french_prob:
                    output.write("Italian\n")
                else:
                    output.write("French\n")
            else:
                output.write("English\n")

        output.close()

    file1 = set()
    file2 = set()
    # read file as plain text
    with open("LangId.sol", 'r') as f:
        for line in f:
            file1.add(line.strip())
    # im not sure why my file2 is only reading in 3 elements
    # read output file back in to compare
    with open('output_file1.txt', 'r') as f:
        for line in f:
            file2.add(line.strip())
    print(len(file1 - file2)/len(file1))
    print(file1 - file2)
