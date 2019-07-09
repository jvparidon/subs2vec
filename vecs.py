# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import pandas as pd
import argparse
import similarities
import analogies
from utensils import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


class Vectors:
    @log_timer
    def __init__(self, fname, normalize=False, n=1e6, d=300):
        n = int(n)
        logging.info(f'loading vectors {fname}')

        with open(fname, 'r', encoding='utf-8') as vecfile:
            # skip header
            next(vecfile)

            # initialize arrays
            self.vectors = np.zeros((n, d))
            self.words = np.empty(n, dtype=object)

            # fill arrays
            for i, line in enumerate(vecfile):
                if i >= n:
                    break
                rowentries = line.rstrip('\n').split(' ')
                self.words[i] = rowentries[0]
                self.vectors[i] = rowentries[1:d + 1]

            # truncate empty part of arrays, if necessary
            self.vectors = self.vectors[:i]
            self.words = self.words[:i]

            # normalize by L1 norm
            if normalize:
                self.vectors = self.vectors / np.linalg.norm(self.vectors, axis=1).reshape(-1, 1)

    @log_timer
    def as_df(self):
        return pd.DataFrame(self.vectors).set_index(self.words)


def load_vecs(fname, normalize=False, n=False, d=300):
    def normalize_vec(x):
        return x / np.linalg.norm(x)
    logging.info(f'loading vecs {fname}')
    vecs_dict = {}
    with open(fname, 'r', encoding='utf-8') as vecfile:
        i = 0
        for line in vecfile:
            line = line.rstrip('\n').split(' ')
            if len(line) > d:
                if normalize:
                    vecs_dict[line[0]] = normalize_vec(np.array([float(num) for num in line[1:d + 1]]))
                else:
                    vecs_dict[line[0]] = np.array([float(num) for num in line[1:d + 1]])
            i += 1
            if n and (i > n):
                return vecs_dict
    return vecs_dict


def write_vecs(vecs, fname):
    with open(fname, 'w') as vecfile:
        for key, value in vecs.items():
            vecfile.write(f'{key} {" ".join([str(num) for num in value])}\n')


def print_result(results):
    results = [str(result) for result in results]
    print('\t'.join(results))


def print_result_pretty(label, result, t=0):
    if t > 0:
        print('{: <50}{: 5.2f} ({: >5}/{: >5}) in {}s'.format(label, *result, int(t)))
    else:
        print('{: <50}{: 5.2f} ({: >5}/{: >5})'.format(label, *result))


def evaluate_vecs(vecs_dict, lang, no_similarities=False, no_analogies=False):
    if no_similarities:
        logging.info('skipping similarities')
    else:
        similarities.evaluate_vecs(vecs_dict, lang)
    if no_analogies:
        logging.info('skipping analogies')
    else:
        analogies.evaluate_vecs(vecs_dict, lang)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='evaluate a set of word embeddings')
    argparser.add_argument('--filename',
                           help='word vectors to evaluate')
    argparser.add_argument('--lang', default='en',
                           help='language to evaluate vector in (use ISO 639-1 codes)')
    argparser.add_argument('--no_similarities', action='store_true',
                           help='do not include semantic similarity correlations')
    argparser.add_argument('--no_analogies', action='store_true',
                           help='do not include analogy problems')
    args = argparser.parse_args()

    vecs_dict = load_vecs(args.filename, n=1e6, normalize=True)
    evaluate_vecs(vecs_dict,
                  lang=args.lang,
                  no_similarities=args.no_similarities,
                  no_analogies=args.no_analogies)
