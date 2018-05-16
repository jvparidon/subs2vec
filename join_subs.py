# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
import argparse
import unicodedata
import string
import sys
import numpy as np
from utensilities import timer


punctuation = string.punctuation.replace('_', '')
punctuation_table = str.maketrans(punctuation, ' ' * len(punctuation))
def strip_punctuation(text, lower=False):
    if lower:
        lines = [' '.join([word for word in line.split(' ') if word != '']) for line in text.lower().translate(punctuation_table).replace('_punct', '').split('\n')]
    else:
        lines = [' '.join([word for word in line.split(' ') if word != '']) for line in text.translate(punctuation_table).replace('_punct', '').split('\n')]
    return '\n'.join([line for line in lines if line != ''])


@timer
def join_dir(in_dir, out_dir, lang, verbose=False, ioformat='txt'):
    filepaths = []
    for root, dirnames, filenames in os.walk(os.path.join(in_dir, lang)):
        for filename in filenames:
            if filename.endswith('.{}'.format(ioformat)):
                filepaths.append(os.path.join(root, filename))
    total = len(filepaths)
    i = 0
    out_fname = os.path.join(out_dir, '{}.{}'.format(lang, ioformat))
    with open(out_fname, 'w') as outfile:
        for filepath in filepaths:
            with open(filepath, 'r') as infile:
                outfile.write(strip_punctuation(infile.read()))
                if verbose:
                    i += 1
                    print('writing xml-stripped text files to single training file: {:5.2f}%'.format((float(i) / total) * 100), end='\r')
    if verbose:
        print('')
    return total


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='join xml-stripped text files into a single training file for word2vec-style models')
    parser.add_argument('--in_dir', default='../OpenSubtitles2018/raw', help='directory the files are located in')
    parser.add_argument('--out_dir', default='../training_data/opensubtitles/raw', help='directory the output will be written to')
    parser.add_argument('--ioformat', default='txt', choices=['txt', 'lemma', 'upos', 'viz'], help='input/output format')
    parser.add_argument('--verbose', default='False')
    args = parser.parse_args()

    in_dir = args.in_dir
    out_dir = args.out_dir
    ioformat = args.ioformat
    verbose = args.verbose
    for lang in sorted(os.listdir(in_dir)):
        if '.' not in lang:
            results, t = join_dir(in_dir, out_dir, lang, verbose=verbose, ioformat=ioformat)
            print('joined {} files for language {} in {} seconds'.format(results, lang, int(t['duration'])))
