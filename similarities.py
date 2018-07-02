# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import pandas as pd
import argparse
import os
import scipy.spatial.distance
import scipy.stats
import vecs
from utensilities import timer


@timer
def compare_similarities(fname, vecs_dict):
    wordsim = pd.read_csv(fname, delimiter='\t', comment='#')
    sub2vec_dsm = []
    wordsim_dsm = []
    for index, pair in wordsim.iterrows():
        if all(word in vecs_dict.keys() for word in (pair['word1'], pair['word2'])):
            sub2vec_dsm.append(scipy.spatial.distance.cosine(vecs_dict[pair['word1']], vecs_dict[pair['word2']]))
            wordsim_dsm.append(pair['similarity'])
    return scipy.stats.spearmanr(wordsim_dsm, sub2vec_dsm)[0], len(wordsim_dsm), len(wordsim)


def evaluate_vecs(vecs_dict, lang, verbose=True):
    folder = 'evaluation/similarities'
    results = []
    for fname in sorted(os.listdir(folder)):
        if fname.lower().startswith(lang):
            result, t = compare_similarities(os.path.join(folder, fname), vecs_dict)
            results.append((fname, result, t['duration']))
            if verbose:
                vecs.print_result(fname, result, t['duration'])
    return results


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='compute semantic similarity correlations')
    argparser.add_argument('--filename', help='word vectors to evaluate')
    argparser.add_argument('--lang', help='language to compare simarities in (use ISO 639-1 codes)')
    args = argparser.parse_args()

    vecs_dict = vecs.load_vecs(args.filename, n=1e6)
    results = evaluate_vecs(vecs_dict, args.lang)
