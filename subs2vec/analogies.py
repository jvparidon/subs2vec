"""Evaluate word vectors by solving syntactic and semantic analogies."""
import numpy as np
import pandas as pd
import argparse
import os
from .utensils import log_timer
from .vecs import Vectors
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


@log_timer
def solve_analogies(analogies, vectors, method='multiplicative', whole_matrix=False):
    """Solves analogies using specified methods.
    
    :param analogies: list of analogies
    :param vectors: Vectors object containing word vectors
    :param method: solving method to use (options are "additive" and "multiplicative", multiplicative is the default and usually performs best)
    :param whole_matrix: boolean determining whether to use whole matrix multiplication (faster, but uses more RAM than you may have available, False is the default)
    :return: tuple of (fraction of analogies solved correctly, number of analogies with no missing vectors, total number of analogies)
    """
    missing = 0
    total = len(analogies)
    vecs_dict = vectors.as_dict()

    # make numpy arrays of vecs for given words in analogies
    a1 = []
    a2 = []
    b1 = []
    b2_words = []
    analogies_words = []

    for idx, analogy in analogies.iterrows():
        if all(word in vecs_dict.keys() for word in analogy.values):
            a1.append(vecs_dict[analogy['a1']])
            a2.append(vecs_dict[analogy['a2']])
            b1.append(vecs_dict[analogy['b1']])
            b2_words.append(analogy['b2'])
            analogies_words.append([analogy['a1'], analogy['a2'], analogy['b1']])
        else:
            missing += 1
    a1 = np.vstack(a1)
    a2 = np.vstack(a2)
    b1 = np.vstack(b1)
    b2_words = np.vstack(b2_words)
    analogies_words = np.vstack(analogies_words)
    l = len(analogies_words)

    # cosine distance (assumes vectors are normalized to unit length)
    def cos(a, b):
        return np.matmul(a, b.T)

    # cosine similarity (assumes vectors are normalized to unit length)
    def cos_pos(a, b):
        return (1.0 + np.matmul(a, b.T)) / 2.0

    # compute cosine similarity between all word vecs and
    # the vecs predicted from the word word analogy arrays
    if method == 'multiplicative':
        # multiplicative method from Levy & Goldberg (2014)
        eps = np.finfo(np.float64).eps
        if whole_matrix:
            logging.info('computing analogies using whole matrix multiplicative method')
            b2_pred = ((cos_pos(vectors.vectors, b1) * cos_pos(vectors.vectors, a2)) / (cos_pos(vectors.vectors, a1) + eps))
            test1 = b2_pred
            # zero out other words in analogy (yes, this feels like cheating)
            for i in range(l):
                b2_pred[np.isin(vectors.words, analogies_words[i]), i] = -1.0
            b2_pred_idx = np.argmax(b2_pred, axis=0)
        else:
            logging.info('computing analogies using linewise multiplicative method')
            b2_pred_idx = np.zeros(l, dtype=np.int32)
            for i in range(l):
                b2_pred = ((cos_pos(vectors.vectors, b1[i].reshape(1, -1)) * cos_pos(vectors.vectors, a2[i].reshape(1, -1)))
                           / (cos_pos(vectors.vectors, a1[i].reshape(1, -1)) + eps)).squeeze()
                # zero out other words in analogy (yes, this feels like cheating)
                test2 = b2_pred
                b2_pred[np.isin(vectors.words, analogies_words[i])] = -1.0
                b2_pred_idx[i] = np.argmax(b2_pred)

    elif method == 'additive':
        # additive method from Mikolov et al. (2013)
        # consider this method deprecated in favor of the multiplicative method
        if whole_matrix:
            logging.info('computing analogies using whole matrix additive method')
            b2_pred = cos(vectors.vectors, b1 - a1 + a2)
            # zero out other words in analogy (yes, this feels like cheating)
            for i in range(l):
                b2_pred[np.isin(vectors.words, analogies_words[i])] = -1.0
            b2_pred_idx = np.argmax(b2_pred, axis=0)
        else:
            logging.info('computing analogies using linewise additive method')
            b2_pred_idx = np.zeros(l, dtype=np.int32)
            for i in range(l):
                b2_pred = cos(vectors.vectors, (b1[i] - a1[i] + a2[i]).reshape(1, -1)).squeeze()
                # zero out other words in analogy (yes, this feels like cheating)
                b2_pred[np.isin(vectors.words, analogies_words[i])] = -1.0
                b2_pred_idx[i] = np.argmax(b2_pred)

    return np.mean(vectors.words[b2_pred_idx] == b2_words.squeeze()), total - missing, total


@log_timer
def evaluate_vecs(vectors, lang, method='multiplicative', whole_matrix=False):
    """Solve all available analogies for a set of word vectors in a given language.

    :param vectors: Vectors object containing word vectors
    :param lang: language to evaluate word vectors in (uses two-letter ISO codes)
    :param method: solving method to use (options are "additive" and "multiplicative", multiplicative is the default and usually performs best)
    :param whole_matrix: boolean determining whether to use whole matrix multiplication (faster, but uses more RAM than you may have available, False is the default)
    :return: list of results
    """
    results = []
    folder = 'evaluation/datasets/analogies'
    for fname in sorted(os.listdir(folder)):
        if fname.startswith(lang) and fname.endswith('.tsv'):
            analogies = pd.read_csv(os.path.join(folder, fname), sep='\t', comment='#')
            result = solve_analogies(analogies, vectors, method=method, whole_matrix=whole_matrix)
            result = (fname, *result)
            # TODO: fix results printing
            vecs.print_result(result)
            results.append(result)
    return results


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='solve syntactic and semantic analogies from Mikolov et al. (2013)')
    argparser.add_argument('--fname', help='word vectors to evaluate')
    argparser.add_argument('--lang', help='language to solve analogies in (use ISO 639-1 codes)')
    argparser.add_argument('--whole_matrix', action='store_true',
                           help='perform computations using whole matrices instead of column-wise (potentially results in big memory footprint)')
    args = argparser.parse_args()

    vectors = Vectors(args.fname, normalize=True, n=2e5)
    results = evaluate_vecs(vectors, lang=args.lang, whole_matrix=args.whole_matrix)
