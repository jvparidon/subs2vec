# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
import lzma
from utensilities import timer


def get_lines(fhandle):
    lines = fhandle.read().split('\n')
    n_lines = len(lines)
    lines = set(lines)
    n_duplicates = n_lines - len(lines)
    return lines, n_lines, n_duplicates


@timer
def dedup_file(in_fname, out_fname):
    with open(in_fname, 'r') as in_file, open(out_fname, 'w') as out_file:
        lines, n_lines, n_duplicates = get_lines(in_file)
        out_file.write('\n'.join(lines))
    return n_lines, n_duplicates


def dedup_reddit(folder, verbose=False):
    fnames = [os.path.join(folder, fname) for fname in sorted(list(os.listdir(folder))) if
              fname.endswith('_stripped.txt')]
    for fname in fnames:
        with open(fname, 'rt') as in_file, open('{}.dedup.txt'.format(fname[:-4]), 'w') as out_file:
            lines, n_lines, n_duplicates = get_lines(in_file)
            out_file.write('\n'.join(lines))
        if verbose:
            print('removed {} duplicates from {} lines in file {}'.format(n_duplicates, n_lines, fname))


if __name__ == '__main__':
    # for deduplicating reddit corpus without memory overruns, deduplicate by month first, then by year, then overall?
    #n_lines, n_duplicates, t = dedup_file('../reddit/reddit_comments.txt', '../reddit/reddit_comments.dedup.txt')
    #print('read {} lines and removed {} duplicates in {} seconds'.format(n_lines, n_duplicates, int(t['duration'])))
    dedup_reddit('../reddit/stripped', verbose=True)
