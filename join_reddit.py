# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import os
from utensilities import timer


@timer
def join_files(folder):
    fnames = [os.path.join(folder, fname) for fname in sorted(list(os.listdir(folder))) if fname.endswith('_stripped..dedup.txt')]
    with open(os.path.join(folder, 'reddit_comments.txt'), 'w') as training_file:
        for fname in fnames:
            print('writing file {} to reddit training file'.format(fname))
            with open(fname, 'r') as comment_file:
                training_file.write(comment_file.read())
    return len(fnames)


if __name__ == '__main__':
    folder = '../reddit/stripped2'
    results, t = join_files(folder)
    print('joined {} reddit comment files in {} seconds'.format(results, int(t['duration'])))
