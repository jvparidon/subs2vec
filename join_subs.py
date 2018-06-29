# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
import argparse
import unicodedata
import string
import sys
import numpy as np
from utensilities import timer


def strip_special(txt):
    return ''.join([char if char.isalnum() else ' ' for char in txt])


def strip_punctuation(txt):
    lines = [' '.join([word for word in strip_special(line).split(' ') if word != '']) for line in txt.split('\n')]
    return '{}\n'.format('\n'.join([line for line in lines if line != '']))


@timer
def join_dir(in_dir, out_dir, lang, verbose=False, ioformat='txt', subset_years=(0, 2020)):
    out_fname = os.path.join(out_dir, '{}.{}-{}.{}'.format(lang, *subset_years, ioformat))
    filepaths = []
    for year in sorted(os.listdir(os.path.join(in_dir, lang))):
        if int(year) in range(*subset_years):
            for root, dirnames, filenames in os.walk(os.path.join(in_dir, lang, year)):
                for filename in filenames:
                    if filename.endswith('.{}'.format(ioformat)):
                        filepaths.append(os.path.join(root, filename))
    total = len(filepaths)
    i = 0
    with open(out_fname, 'w') as outfile:
        for filepath in filepaths:
            with open(filepath, 'r') as infile:
                outfile.write(strip_punctuation(infile.read()))
                if verbose:
                    i += 1
                    print('writing xml-stripped text files to single training file: {:5.2f}%'
                          .format((float(i) / total) * 100), end='\r')
    if verbose:
        print('')
    return total


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='join xml-stripped text files into a single training file for word2vec-style models')
    argparser.add_argument('--lang', default='en',
                           help='source language (OpenSubtitles data uses ISO 3166-1)')
    argparser.add_argument('--in_dir', default='../OpenSubtitles2018/raw',
                           help='directory the files are located in')
    argparser.add_argument('--out_dir', default='../training_data/opensubtitles/raw',
                           help='directory the output will be written to')
    argparser.add_argument('--ioformat', default='txt', choices=['txt', 'lemma', 'upos', 'viz'],
                           help='input/output format')
    argparser.add_argument('--verbose', default='True')
    args = argparser.parse_args()

    results, t = join_dir(**vars(args))
    print('joined {} files in {} seconds'.format(results, int(t['duration'])))
