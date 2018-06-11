# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import argparse
from utensilities import timer
import vecs


def get_analogies(analogies_set, lang='en', subsets=False):
    if analogies_set == 'syntactic':
        fname = '../google_analogies/{}-syntactic.txt'.format(lang)
    elif analogies_set == 'semantic':
        fname = '../google_analogies/{}-semantic.txt'.format(lang)
    with open(fname, 'r') as analogies_file:
        if subsets:
            analogies = {}
            for line in analogies_file:
                if ':' in line:
                    subset = line.strip('\n')
                    analogies[subset] = []
                else:
                    analogies[subset].append(line.strip('\n').split(' '))
        else:
            analogies = [line.strip('\n').split(' ') for line in analogies_file
                         if line[0] != ':']
    return analogies


@timer
def solve_analogies(analogies, vecs_dict, method='additive',
                    whole_matrix=False):
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
            b2_pred = ((cos_pos(vecs, b1) * cos_pos(vecs, a2))
                       / (cos_pos(vecs, a1) + eps))
            # zero out b1s (yes, this feels like cheating)
            for i in range(len(b1_words)):
                b2_pred[np.isin(words.squeeze(), analogies[i][0:3])] = -1.0
            b2_pred_idx = np.argmax(b2_pred, axis=0)
        else:
            b2_pred_idx = np.zeros(b1.shape[0], dtype=np.int32)
            for i in range(b1.shape[0]):
                b2_pred = ((cos_pos(vecs, b1[i].reshape(1, -1))
                            * cos_pos(vecs, a2[i].reshape(1, -1)))
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
                  lang='en',
                  analogies_types=['syntactic', 'semantic'],
                  methods=['additive', 'multiplicative'],
                  subsets=False,
                  whole_matrix=False,
                  verbose=True):
    results = []
    for analogies_type in analogies_types:
        analogies = get_analogies(analogies_type, lang, subsets)
        for method in methods:
            if subsets:
                for subset in sorted(analogies.keys()):
                    result, t = solve_analogies(analogies[subset], vecs_dict,
                                                method=method,
                                                whole_matrix=whole_matrix)
                    label = '{} ({})'.format(subset[2:], method)
                    results.append((label, result, t['duration']))
                    if verbose:
                        vecs.print_result(label, result, t['duration'])
            else:
                result, t = solve_analogies(analogies, vecs_dict, method=method,
                                            whole_matrix=whole_matrix)
                label = '{} ({})'.format(analogies_type, method)
                results.append((label, result, t['duration']))
                if verbose:
                    vecs.print_result(label, result, t['duration'])
    return results


if __name__ == '__main__':
    #vecs_fname = '../tmp-jeroen/en.dedup.5pass.d5.t100.vec'
    #vecs_fname = '../pretrained/mkb2017.vec'
    #vecs_fname = '../pretrained/fasttext/crawl-300d-2M.vec'
    #vecs_fname = '../pretrained/fasttext/wiki-news-300d-1M-subword.vec'
    #vecs_fname = '../tmp-jeroen/fr.dedup.5pass.d5.t100.vec'
    vecs_fname = '../tmp-jeroen/pl.dedup.5pass.d5.t100.vec'
    #vecs_fname = '../pretrained/fasttext/cc.fr.300.vec'
    #vecs_fname = '../reddit/reddit.dedup.sg.lr01.vec'

    argparser = argparse.ArgumentParser(
        description='solve syntactic and semantic analogies from Mikolov et al.'
                    + ' (2013)')
    argparser.add_argument('--filename', default=vecs_fname,
        help='word vectors to evaluate')
    argparser.add_argument('--lang', default='en',
                           choices=['en', 'fr', 'hi', 'pl'],
        help='language to solve analogies in (uses ISO 3166-1 codes)')
    argparser.add_argument('--subsets', default=False, type=bool,
        help='break syntactic/semantic analogy performance down by subset')
    argparser.add_argument('--whole_matrix', default=False, type=bool,
        help='perform computations using whole matrices instead of column-wise'
             + ' (potentially results in massive memory use)')
    args = argparser.parse_args()

    vecs_dict = vecs.load_vecs(args.filename, normalize=True, n=1e6)
    results = evaluate_vecs(vecs_dict, lang=args.lang, subsets=args.subsets,
                            whole_matrix=args.whole_matrix)
