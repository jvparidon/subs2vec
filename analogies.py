# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import argparse
import os
from utensils import timer
import vecs
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


def get_analogies(fname, subsets=False):
    with open(fname, 'r') as analogies_file:
        if subsets:
            analogies = {}
            for line in analogies_file:
                line = line.lower()  # important if the word vectors are lowercased
                if line.startswith(':'):
                    subset = line.strip('\n')
                    analogies[subset] = []
                else:
                    analogies[subset].append(line.strip('\n').split(' '))
        else:
            analogies = [line.lower().strip('\n').split(' ') for line in analogies_file
                         if line[0] != ':']
    return analogies


@timer
def solve_analogies(analogies, vecs_dict, method='additive', whole_matrix=False):
    missing = 0
    total = len(analogies)
    # make numpy arrays of vecs for given words in analogies
    a1 = []
    a2 = []
    b1 = []
    b1_words = []
    b2_targets = []
    for analogy in analogies:
        if all(word in vecs_dict.keys() for word in analogy):
            a1 += [vecs_dict[analogy[0]]]
            a2 += [vecs_dict[analogy[1]]]
            b1 += [vecs_dict[analogy[2]]]
            b1_words += [analogy[2]]
            b2_targets += [analogy[3]]
        else:
            missing += 1
    a1 = np.vstack(a1)
    a2 = np.vstack(a2)
    b1 = np.vstack(b1)
    b1_words = np.vstack(b1_words)
    b2_targets = np.vstack(b2_targets)
    # make numpy array of all word vecs and an index/word array
    words = []
    vecs = []
    for key, value in vecs_dict.items():
        words += [key]
        vecs += [value]
    words = np.vstack(words)
    vecs = np.vstack(vecs)

    # cosine similarity (assumes vectors are normalized to unit length)
    def cos(a, b):
        return np.matmul(a, b.T)

    def cos_pos(a, b):
        return (1.0 + np.matmul(a, b.T)) / 2.0

    # compute cosine distance between all word vecs and
    # the vecs predicted from the word word analogy arrays
    if method == 'multiplicative':
        # multiplicative method from Levy & Goldberg (2014)
        eps = np.finfo(np.float64).eps
        if whole_matrix:
            b2_pred = ((cos_pos(vecs, b1) * cos_pos(vecs, a2)) / (cos_pos(vecs, a1) + eps))
            # zero out b1s (yes, this feels like cheating)
            for i in range(len(b1_words)):
                b2_pred[np.isin(words.squeeze(), analogies[i][0:3])] = -1.0
            b2_pred_idx = np.argmax(b2_pred, axis=0)
        else:
            b2_pred_idx = np.zeros(b1.shape[0], dtype=np.int32)
            for i in range(b1.shape[0]):
                b2_pred = ((cos_pos(vecs, b1[i].reshape(1, -1)) * cos_pos(vecs, a2[i].reshape(1, -1)))
                           / (cos_pos(vecs, a1[i].reshape(1, -1)) + eps)).squeeze()
                # zero out b1s (yes, this feels like cheating)
                b2_pred[np.isin(words, analogies[i][0:3]).squeeze()] = -1.0
                b2_pred_idx[i] = np.argmax(b2_pred)

    elif method == 'additive':
        # additive method from Mikolov et al. (2013)
        if whole_matrix:
            b2_pred = cos(vecs, b1 - a1 + a2)
            # zero out b1s (yes, this feels like cheating)
            for i in range(len(b1_words)):
                b2_pred[np.isin(words.squeeze(), analogies[i][0:3])] = -1.0
            b2_pred_idx = np.argmax(b2_pred, axis=0)
        else:
            b2_pred_idx = np.zeros(b1.shape[0], dtype=np.int32)
            for i in range(b1.shape[0]):
                b2_pred = cos(vecs, (b1[i] - a1[i] + a2[i]).reshape(1, -1)).squeeze()
                # zero out b1s (yes, this feels like cheating)
                b2_pred[np.isin(words.squeeze(), analogies[i][0:3])] = -1.0
                b2_pred_idx[i] = np.argmax(b2_pred)

    b2_pred_words = words[b2_pred_idx]
    return np.mean(b2_pred_words == b2_targets), total - missing, total


def evaluate_vecs(vecs_dict,
                  lang,
                  analogies_type='',
                  methods=['multiplicative'],
                  subsets=False,
                  whole_matrix=False):
    results = []
    folder = 'evaluation/analogies'
    for fname in sorted(os.listdir(folder)):
        if fname.startswith(lang) and (analogies_type in fname):
            analogies = get_analogies(os.path.join(folder, fname), subsets)
            for method in methods:
                if subsets:
                    for subset in sorted(analogies.keys()):
                        result, t = solve_analogies(analogies[subset], vecs_dict, method=method, whole_matrix=whole_matrix)
                        result = (subset[2:], *result, t['duration'], method)
                        vecs.print_result(result)
                        results.append(result)
                else:
                    result, t = solve_analogies(analogies, vecs_dict, method=method, whole_matrix=whole_matrix)
                    result = (fname, *result, t['duration'], method)
                    vecs.print_result(result)
                    results.append(result)
    return results


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='solve syntactic and semantic analogies from Mikolov et al. (2013)')
    argparser.add_argument('--filename',
                           help='word vectors to evaluate')
    argparser.add_argument('--lang', default='en',
                           help='language to solve analogies in (use ISO 639-1 codes)')
    argparser.add_argument('--subsets', default=False, type=bool,
                           help='break syntactic/semantic analogy performance down by subset')
    argparser.add_argument('--whole_matrix', default=False, type=bool,
                           help='perform computations using whole matrices instead of column-wise'
                                + ' (potentially results in massive memory use)')
    args = argparser.parse_args()

    vecs_dict = vecs.load_vecs(args.filename, normalize=True, n=1e6)
    results = evaluate_vecs(vecs_dict, lang=args.lang, subsets=args.subsets, whole_matrix=args.whole_matrix)
