# -*- coding: utf-8 -*-
# jvparidon@gmail.com
from __future__ import print_function
import os
import unicodedata
import string
import sys
import numpy as np
from utensilities import timer


'''
punctuation = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P'))
numerals = {
    '0': 'zero',
    '1': 'one',
    '2': 'two',
    '3': 'three',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'nine',
}
'''
punctuation_table = string.maketrans(string.punctuation, ' ' * len(string.punctuation))
def strip_punctuation(text):
    lines = [' '.join([word for word in line.split(' ') if word != '']) for line in text.lower().translate(punctuation_table).split('\n')]
    return '\n'.join([line for line in lines if line != ''])


@timer
def join_txts(folder, verbose=False):
    filepaths = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.txt'):
                filepaths.append(os.path.join(root, filename))
    total = len(filepaths)
    i = 0
    with open(folder + '.txt', 'w') as outfile:
        for filepath in filepaths:
            with open(filepath, 'r') as infile:
                outfile.write(strip_punctuation(infile.read()))
                if verbose:
                    i += 1
                    print('writing txts to single training txt: {}%'.format(int((float(i) / total) * 100)), end='\r')
    print()
    return total


if __name__ == '__main__':
    results, t = join_txts('OpenSubtitles2018/raw/nl', verbose=True)
    print('joined {} files in {} seconds'.format(results, int(t['duration'])))
