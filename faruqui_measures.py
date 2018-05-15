# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import pandas
import argparse
import os
import scipy.spatial.distance
import scipy.stats
from vecs import load_vecs, sub2vec_dissim


def compare_dissimilarities(fname, vecs_dict):
    with open(fname, 'r') as simfile:
        lines = simfile.read()
    lines = [line.split() for line in lines.split('\n')[:-1]]
    word_pairs = [(line[0], line[1]) for line in lines]
    wordsim = [line[2] for line in lines]
    sub2vec_dsm = []
    wordsim_dsm = []
    for i in range(len(word_pairs)):
        try:
            sub2vec_dsm.append(sub2vec_dissim(word_pairs[i], vecs_dict))
            wordsim_dsm.append(wordsim[i])
            #print('{} {} {}'.format(word_pairs[i][0], word_pairs[i][1], wordsim[i]))
        except KeyError:
            pass
    return fname, np.around(scipy.stats.spearmanr(wordsim_dsm, sub2vec_dsm)[0], 3), len(wordsim_dsm), len(word_pairs)


def evaluate_vecs(vecs_dict, verbose=True):
    folder = '../faruqui_dissimilarities'
    results = []
    for filename in sorted(os.listdir(folder)):
        results.append(compare_dissimilarities(os.path.join(folder, filename), vecs_dict))
    if verbose=True:
        [print('{: <45} {: >6} ({}/{})'.format(*entry)) for entry in results]
    return results


if __name__ == '__main__':
    #vecs_file = '../results/en/sub.en.vec'
    #vecs_file = '../results/en/sub.lemma.en.vec'
    #vecs_file = '../pretrained_reference/fasttext/wiki.en.vec'
    #vecs_file = '../cbow_models/sub.en.defaults.vec'
    #vecs_file = '../pretrained_reference/fasttext/wiki-news-300d-1M-subword.vec'
    #vecs_file = '../pretrained_reference/fasttext/crawl-300d-2M.vec'
    #vecs_file = '../pretrained_reference/glove.840B.300d.txt'
    vecs_file = '../pretrained_reference/mkb2017.vec'

    argparser = argparse.ArgumentParser(description='Run evaluation metrics from wordvectors.org')
    argparser.add_argument('--filename', default=vecs_file, help='word vectors to evaluate')
    args = argparser.parse_args()

    vecs_dict = load_vecs(args.filename)
    results = evaluate_vecs(vecs_dict)
