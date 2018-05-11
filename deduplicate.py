# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
from utensilities import timer


def get_lines(fname, verbose=True):
    with open(fname, 'r') as training_file:
        lines = training_file.read().split('\n')
        n_lines = len(lines)
        lines = set(lines)
        n_duplicates = n_lines - len(lines)
    return lines, n_lines, n_duplicates


def write_dedup(fname, lines):
    with open(fname, 'w') as dedup_file:
        dedup_file.write('\n'.join(lines))


@timer
def dedup_file(in_fname, out_fname):
    lines, n_lines, n_duplicates = get_lines(in_fname)
    write_dedup(out_fname, lines)
    return n_lines, n_duplicates


if __name__ == '__main__':
    # for deduplicating reddit corpus without memory overruns, deduplicate by month first, then by year, then overall?
    n_lines, n_duplicates, t = dedup_file('../training_data/opensubtitles/raw/en.txt', '../dedup.en.txt')
    print('read {} lines and removed {} duplicates in {} seconds'.format(n_lines, n_duplicates, int(t['duration'])))
