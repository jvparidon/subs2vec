# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import argparse
import os
import scipy.spatial.distance
import scipy.stats
import vecs
from utensilities import timer


@timer
def compare_dissimilarities(fname, vecs_dict):
    with open(fname, 'r') as simfile:
        lines = simfile.read()
    lines = [line.split() for line in lines.split('\n')[:-1]]
    word_pairs = [(line[0], line[1]) for line in lines]
    wordsim = [line[2] for line in lines]
    sub2vec_dsm = []
    wordsim_dsm = []
    for i in range(len(word_pairs)):
        if all(word in vecs_dict.keys() for word in word_pairs[i]):
            sub2vec_dsm.append(scipy.spatial.distance.cosine(vecs_dict[word_pairs[i][0]], vecs_dict[word_pairs[i][1]]))
            wordsim_dsm.append(wordsim[i])
    return scipy.stats.spearmanr(wordsim_dsm, sub2vec_dsm)[0], len(wordsim_dsm), len(word_pairs)


def evaluate_vecs(vecs_dict, verbose=True):
    folder = 'faruqui_dissimilarities'
    results = []
    for fname in sorted(os.listdir(folder)):
        result, t = compare_dissimilarities(os.path.join(folder, fname), vecs_dict)
        results.append((fname, result, t['duration']))
        if verbose:
            vecs.print_result(fname, result, t['duration'])
    return results


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='compute semantic dissimilarity correlations from wordvectors.org')
    argparser.add_argument('--filename', help='word vectors to evaluate')
    args = argparser.parse_args()

    vecs_dict = vecs.load_vecs(args.filename)
    results = evaluate_vecs(vecs_dict)
