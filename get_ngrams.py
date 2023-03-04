import sys
import os
import nltk
import pickle
from nltk import word_tokenize
from nltk import ngrams


def read_data(file_path):
    # Reads file from specified file path, returns file text
    with open(os.path.join(os.getcwd(), file_path), "r", encoding = "utf-8") as f:
        text = f.read()
    return text


def get_count(grams):
    # Creates dictionary of n-grams and the amount of times they appear
    gram_dict = {}
    for gram in grams:
        if gram in gram_dict:
            gram_dict[gram] = gram_dict[gram] + 1
        else:
            gram_dict[gram] = 1
    return gram_dict


def ngram_dicts(filename):
    # Creates lists of unigrams and bigrams, returns dictionaries with counts of each one
    raw_text = read_data(filename)
    unigrams = word_tokenize(raw_text)
    bigrams = list(ngrams(unigrams, 2))

    uni_dict = get_count(unigrams)
    bi_dict = get_count(bigrams)

    print(filename + " complete")
    return uni_dict, bi_dict


if __name__ == '__main__':
    # Read the data and create n-gram dictionaries
    eng_uni, eng_bi = ngram_dicts("data/LangId.train.English")
    fre_uni, fre_bi = ngram_dicts("data/LangId.train.French")
    ita_uni, ita_bi = ngram_dicts("data/LangId.train.Italian")

    # Save the data to pickle files
    pickle.dump(eng_uni, open("eng_uni.p", "wb"))
    pickle.dump(eng_bi, open("eng_bi.p", "wb"))
    pickle.dump(fre_uni, open("fre_uni.p", "wb"))
    pickle.dump(fre_bi, open("fre_bi.p", "wb"))
    pickle.dump(ita_uni, open("ita_uni.p", "wb"))
    pickle.dump(ita_bi, open("ita_bi.p", "wb"))