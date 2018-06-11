# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import json
import os
import bz2
import lzma
import re
import string
import html
from joblib import Parallel, delayed
from utensilities import timer
from multiprocessing import cpu_count
cores = int(cpu_count() / 2)


def strip_special(txt):
    return ''.join([char if char.isalnum() else ' ' for char in txt])


def strip_line(line):
    lines = [' '.join([word for word in strip_special(line).split(' ') if word != '']) for line in
             re.sub(r'http\S+', '', html.unescape(json.loads(line)['body'])).split('\n')]
    return '{}\n'.format('\n'.join([line for line in lines if line != '']))


def strip_file(fname, compress=True):
    filewriter = lzma.open if compress else open
    ext_new = '_stripped.xz' if compress else '_stripped.txt'
    if fname.endswith('.bz2'):
        fileopener = bz2.open
        ext = '.bz2'
    elif fname.endswith('.xz'):
        fileopener = lzma.open
        ext = '.xz'
    elif fname.endswith('.json'):
        fileopener = open
        ext = '.json'
    else:
        return False
    with fileopener(fname, 'rt') as json_file, filewriter(fname.replace(ext, ext_new), 'wt') as stripped_file:
        i = 0
        for line in json_file:
            try:
                stripped_file.write(strip_line(line))
            except json.JSONDecodeError:
                print('encountered invalid JSON in file {} on line {}'.format(fname, i))
            i += 1
    print('successfully stripped file {}'.format(fname))
    return True


def strip_folder_parallel(folder, compress=True, cores=1):
    fnames = [os.path.join(folder, fname) for fname in sorted(list(os.listdir(folder))) if
              (fname.endswith('.bz2') or fname.endswith('.xz'))]
    return strip_parallelized(fnames, compress, cores)


@timer
def strip_parallelized(fnames, compress=True, cores=1):
    return Parallel(n_jobs=cores)(delayed(strip_file)(fname, compress) for fname in fnames)


if __name__ == '__main__':
    folder = '../reddit/other'
    results, t = strip_folder_parallel(folder, compress=False, cores=20)
    print('stripped json from {} files in {} seconds'.format(np.sum(results), int(t['duration'])))
