import pandas as pd
import tensorflow as tf
import numpy as np
import nltk
import string
import re
import keras
import keras.layers as L
import json

from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter
from keras.models import load_model

nltk.download('stopwords')

with open('tokens.json', 'r') as fin:
    TOKEN_TO_ID = json.load(fin)

UNK, PAD = 'UNK', 'PAD'
UNK_IX, PAD_IX = map(TOKEN_TO_ID.get, [UNK, PAD])


def preprocess(data):
    remove = string.punctuation
    pattern = r"[{}]".format(remove)
    stem_ru = SnowballStemmer('russian')
    stem_en = SnowballStemmer('english')

    def stem(x): return stem_ru.stem(stem_en.stem(x))
    tokenizer = WordPunctTokenizer()

    def clean_data(text): return \
        ' '.join([stem(word.lower()) for word in
                  tokenizer.tokenize(re.sub(pattern, "", text))
                  if word not in stopwords.words('russian')
                  and word not in stopwords.words('english')
                  and not word.isdigit()])

    return np.array(list(map(clean_data, data)))


def apply_word_dropout(matrix, keep_prop, replace_ix=UNK_IX, pad_ix=PAD_IX):
    dropout_mask = np.random.choice(
        2, np.shape(matrix), p=[keep_prop, 1 - keep_prop])
    dropout_mask &= matrix != pad_ix
    return np.choose(dropout_mask, [matrix, np.full_like(matrix, replace_ix)])


def as_matrix(sequences, max_len=None):
    if isinstance(sequences[0], str):
        sequences = list(map(str.split, sequences))

    max_len = min(max(map(len, sequences)), max_len or float('inf'))

    matrix = np.full((len(sequences), max_len), np.int32(PAD_IX))
    for i, seq in enumerate(sequences):
        row_ix = [TOKEN_TO_ID.get(word, UNK_IX) for word in seq[:max_len]]
        matrix[i, :len(row_ix)] = row_ix

    return matrix


def make_batch(text, max_len=None, word_dropout=0):
    batch = {}
    text = preprocess(text)
    batch['text'] = as_matrix(text, max_len)
    if word_dropout != 0:
        batch['text'] = apply_word_dropout(batch['text'], 1. - word_dropout)

    return batch
