"""Evaluate word vectors by solving syntactic and semantic analogies."""
import numpy as np
import pandas as pd
import argparse
import os
from .utensils import log_timer
from .vecs import Vectors
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
path = os.path.dirname(__file__)


@log_timer
def solve_analogies(vectors, analogies, method='multiplicative', whole_matrix=False):
    """Solves analogies using specified methods.
    
    :param analogies: pandas DataFrame of analogies, columns labeled a1, a2, b1, b2.
    :param vectors: Vectors object containing word vectors.
    :param method: solving method to use (options are "additive" and "multiplicative", multiplicative is the default and usually performs best).
    :param whole_matrix: boolean determining whether to use whole matrix multiplication (faster, but uses more RAM than you may have available, False is the default).
    :return: dict containing score and predictions in separate pandas DataFrames
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

    # return pandas df with b2 and b2 predicted
    analogies = pd.DataFrame(analogies_words, columns=['a1', 'a2', 'b1'])
    analogies['b2'] = b2_words
    analogies['b2 predicted'] = vectors.words[b2_pred_idx]
    analogies['accuracy'] = analogies['b2'] == analogies['b2 predicted']
    score = analogies['accuracy'].mean()
    corrected_score = score * ((total - missing) / total)
    score = pd.DataFrame([score, corrected_score], columns=['score', 'corrected score'])
    return {'score': score, 'predictions': analogies}
    # return np.mean(vectors.words[b2_pred_idx] == b2_words.squeeze()), total - missing, total


@log_timer
def evaluate_vecs(vecs_fname, lang, method='multiplicative', whole_matrix=False):
    """Solve all available analogies for a set of word vectors in a given language.

    :param vecs_fname: filename of a file containing a set of word vectors
    :param lang: language to evaluate word vectors in (uses two-letter ISO codes)
    :param method: solving method to use (options are "additive" and "multiplicative", multiplicative is the default and usually performs best)
    :param whole_matrix: boolean determining whether to use whole matrix multiplication (faster, but uses more RAM than you may have available, False is the default)
    :return: pandas DataFrame of scores
    """
    analogies_path = os.path.join(path, 'evaluation', 'datasets', 'analogies')
    logging.info(f'evaluating analogy solving with {vecs_fname}')
    vectors = Vectors(vecs_fname, normalize=True, n=2e5, d=300)
    scores = []
    for analogies_fname in os.listdir(analogies_path):
        if analogies_fname.startswith(lang):
            if analogies_fname.startswith(lang) and analogies_fname.endswith('.tsv'):
                logging.info(f'solving analogies from {analogies_fname}')
                analogies = pd.read_csv(os.path.join(analogies_path, analogies_fname), sep='\t', comment='#')
                scores.append(solve_analogies(vectors, analogies, method=method, whole_matrix=whole_matrix)['score'])
    scores_fname = os.path.split(vecs_fname)[1].replace('.vec', '.tsv')
    if len(scores) > 0:
        scores['source'] = analogies_fname
        pd.concat(scores).to_csv(os.path.join(path, 'evaluation', 'results', 'analogies', scores_fname), sep='\t')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='solve syntactic and semantic analogies from Mikolov et al. (2013)')
    argparser.add_argument('lang', help='language to solve analogies in (use ISO 639-1 codes)')
    argparser.add_argument('vecs_fname', help='word vectors to evaluate')
    argparser.add_argument('--whole_matrix', action='store_true',
                           help='perform computations using whole matrices instead of column-wise (potentially results in big memory footprint)')
    args = argparser.parse_args()

    evaluate_vecs(**vars(args))
