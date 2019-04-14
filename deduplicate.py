# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
import lzma
import argparse
import random
from utensilities import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


def get_lines(fhandle):
    lines = fhandle.read().split('\n')
    n_lines = len(lines)
    lines = set(lines)
    n_duplicates = n_lines - len(lines)
    return lines, n_lines, n_duplicates


@log_timer
def dedup_file(in_fname, out_fname):
    with open(in_fname, 'r') as in_file, open(out_fname, 'w') as out_file:
        lines, n_lines, n_duplicates = get_lines(in_file)
        lines = list(lines)
        random.shuffle(lines)
        out_file.write('\n'.join(lines))
    logging.info(f'deduplicated {in_fname}, removed {n_duplicates} duplicates out of {n_lines} lines')
    return n_lines, n_duplicates


def dedup_reddit(folder):
    fnames = [os.path.join(folder, fname) for fname in sorted(list(os.listdir(folder))) if
              fname.endswith('_stripped.txt')]
    for fname in fnames:
        with open(fname, 'rt') as in_file, open('{}.dedup.txt'.format(fname[:-4]), 'w') as out_file:
            lines, n_lines, n_duplicates = get_lines(in_file)
            out_file.write('\n'.join(lines))
            logging.info(f'deduplicated {fname}, removed {n_duplicates} duplicates out of {n_lines} lines')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='deduplicate lines in a file')
    argparser.add_argument('filename', help='file to deduplicate')
    args = argparser.parse_args()

    dedup_file(args.filename, 'dedup.' + args.filename)
