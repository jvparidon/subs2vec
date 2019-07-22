# -*- coding: utf-8 -*-
# jvparidon@gmail.com
"""Compute rank correlations between word vector cosine similarities and human ratings of semantic similarity."""
import numpy as np
import pandas as pd
import argparse
import os
import scipy.spatial.distance
import scipy.stats
import vecs
from utensils import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


def compare_similarities(fname, vecs_dict, replace_missing=True):
    wordsim = pd.read_csv(fname, delimiter='\t', comment='#')
    wordsim['word1'] = wordsim['word1'].str.lower()
    wordsim['word2'] = wordsim['word2'].str.lower()
    sub2vec_dsm = []
    wordsim_dsm = []
    missing = 0

    for index, pair in wordsim.iterrows():
        if all(word in vecs_dict.keys() for word in (pair['word1'], pair['word2'])):
            sub2vec_dsm.append(1.0 - scipy.spatial.distance.cosine(vecs_dict[pair['word1']], vecs_dict[pair['word2']]))
            wordsim_dsm.append(pair['similarity'])
        else:
            missing += 1
            if replace_missing:
                sub2vec_dsm.append(0)
                wordsim_dsm.append(pair['similarity'])

    return scipy.stats.spearmanr(wordsim_dsm, sub2vec_dsm)[0], len(wordsim) - missing, len(wordsim)


@log_timer
def evaluate_vecs(vectors, lang):
    folder = 'evaluation/datasets/similarities'
    results = []
    for fname in sorted(os.listdir(folder)):
        if fname.lower().startswith(lang):
            result = compare_similarities(os.path.join(folder, fname), vectors)
            result = (fname, *result)
            vecs.print_result(result)
            results.append(result)
    return results


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='compute rank correlations between word vector cosine similarities and human semantic similarity ratings')
    argparser.add_argument('--fname', help='word vectors to evaluate')
    argparser.add_argument('--lang', help='language to compare simarities in (use ISO language codes)')
    args = argparser.parse_args()

    vectors = vecs.Vectors(args.fname, normalize=True, n=1e6).as_dict()
    results = evaluate_vecs(vectors, args.lang)
