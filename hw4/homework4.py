from nltk import word_tokenize
from nltk.util import ngrams
import re
import sys
import pickle
import nltk

def read_file(name):
    if len(sys.argv) < 2:
        print("Please enter a filename for system arg")
        quit()

    # read file as plain text
    with open(name, 'r') as f:
        text = f.read()
    return text

def process_data(text):
    # lowercase all text
    text = text.lower()

    # replace newlines with ''
    text = text.replace("\n", "")

    # tokenize text & create unigram
    tokens = text.split()
    # create unigrams list
    unigrams = ngrams(tokens, 1)
    unigrams = [u for u in unigrams if u]

    # create a list of bigrams
    bigrams = list(ngrams(tokens, 2))

    # use list of bigrams to create dict of bigram(token1,token2) and count
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    # use list of unigrams to create dict of unigram and count
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}

    return unigram_dict, bigram_dict


if __name__ == '__main__':
    text1 = read_file('LangId.train.English')
    text2 = read_file('LangId.train.Italian')
    text3 = read_file('LangId.train.French')

    # preprocess data
    uni_dict1, bi_dict1 = process_data(text1)
    uni_dict2, bi_dict2 = process_data(text2)
    uni_dict3, bi_dict3 = process_data(text3)

    dictionaries = [uni_dict1, bi_dict1, uni_dict2, bi_dict2, uni_dict3, bi_dict3]

    # pickle dump all the dictionaries into a pickle file
    # takes a very long time, sorry
    with open('dictionaries1.pickle', 'wb') as handle:
        pickle.dump(dictionaries, handle, pickle.HIGHEST_PROTOCOL)

