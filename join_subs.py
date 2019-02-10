# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
import tarfile
import argparse
import unicodedata
import string
import sys
import numpy as np
from utensilities import timer


def strip_special(txt):
    return ''.join([char if char.isalnum() else ' ' for char in txt])


def strip_punctuation_old(txt):
    lines = [' '.join([word for word in strip_special(line).split(' ') if word != '']) for line in txt.split('\n')]
    return '{}\n'.format('\n'.join([line for line in lines if line != '']))


def strip_punctuation(txt):
    regeces = [
        ('<.*?>', ''),  # strip other xml tags
        ('http.*?(?:[\s\n\]]|$)', ''),  # strip links
        ('([^\s]{2})[\.\?\!]', '\\1\n'),  # line breaks at sentence ends, but not single initials
        ('\n+', '\n'),  # strip excessive line endings
        ('(?:^\n|\n$)', ''),  # strip line endings at either end of strings
        ('[-–]', '-'),  # replace different types of dash with hyphen
        ('[—/]', ' '),  # replace ellipses and slashes with spaces
    ]
    for regec in regeces:
        pattern = re.compile(regec[0], re.IGNORECASE)
        txt = pattern.sub(regec[1], txt)
    txt = ''.join([letter for letter in txt if (letter.isalnum() or letter.isspace() or (letter == '-'))])
    return txt


@timer
def join_dir(tar_filename, out_dir, lang, verbose=False, ioformat='txt', subset_years=False):
    if subset_years:
        out_fname = os.path.join(out_dir, '{}.{}-{}.{}'.format(lang, *subset_years, ioformat))
    else:
        out_fname = os.path.join(out_dir, '{}.{}'.format(lang, ioformat))
        subset_years = (0, 3000)
    tar_object = tarfile.TarFile(tar_filename)
    filepaths = []
    for filepath in sorted(tar_object.getnames()):
        if filepath.endswith('.{}'.format(ioformat)):
            if filepath.startswith('OpenSubtitles2018/raw/' + lang):
                if int(filepath.split('/')[3]) in range(*subset_years):
                    filepaths += [filepath]
    '''
    filepaths = []
    for year in sorted(os.listdir(os.path.join(in_dir, lang))):
        if int(year) in range(*subset_years):
            for root, dirnames, filenames in os.walk(os.path.join(in_dir, lang, year)):
                for filename in filenames:
                    if filename.endswith('.{}'.format(ioformat)):
                        filepaths.append(os.path.join(root, filename))
    '''
    total = len(filepaths)
    i = 0
    with open(out_fname, 'w') as outfile:
        for filepath in filepaths:
            outfile.write(strip_punctuation(tar_object.extractfile(filepath).read().decode('utf-8')))
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
    argparser.add_argument('--tar_filename', default='../OpenSubtitles2018.tar',
                           help='directory the files are located in')
    argparser.add_argument('--out_dir', default='../training_data/opensubtitles/raw',
                           help='directory the output will be written to')
    argparser.add_argument('--ioformat', default='txt', choices=['txt', 'lemma', 'upos', 'viz'],
                           help='input/output format')
    argparser.add_argument('--verbose', default='True')
    args = argparser.parse_args()

    results, t = join_dir(**vars(args))
    print('joined {} files in {} seconds'.format(results, int(t['duration'])))
