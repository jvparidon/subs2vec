"""Find nearest neighbors for words or vectors."""
import numpy as np
import pandas as pd
import argparse
import os
import sklearn.decomposition
from .utensils import log_timer
from .vecs import Vectors
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
path = os.path.dirname(__file__)


@log_timer
def compute_nn(vectors, target_vecs, target_labels, num_neighbors=-1, whole_matrix=False):
    """Solves analogies using specified methods.

    :param vectors: Vectors object containing word vectors
    :param whole_matrix: boolean determining whether to use whole matrix multiplication (faster, but uses more RAM than you may have available, `False` is the default)
    :return: dict containing score and predictions in separate pandas DataFrames
    """
    missing = 0
    total = len(target_labels)
    vecs_dict = vectors.as_dict()

    if target_vecs is None:
        targets = target_labels
        target_labels = []
        target_vecs = []
        for target in targets:
            if target in vecs_dict.keys():
                target_labels.append(target)
                target_vecs.append(vecs_dict[target])
            else:
                missing += 1
        target_vecs = np.vstack(target_vecs)
        target_labels = np.vstack(target_labels)
    l = len(target_vecs)

    # cosine similarity (assumes vectors are normalized to unit length)
    def cos(a, b):
        return np.matmul(a, b.T)

    # alternate formulation for cosine similarity (assumes vectors are normalized to unit length)
    def cos_pos(a, b):
        return (1.0 + np.matmul(a, b.T)) / 2.0

    if whole_matrix:
        logging.info('computing analogies using whole matrix additive method')
        nn_pred = cos(vectors.vectors, target_vecs)
        nn_pred_idx = np.argmax(nn_pred, axis=0)
        if num_neighbors == -1:
            nn_pred_idx = np.argsort(nn_pred, axis=0)[num_neighbors]
            colnames = 'neighbor'
        else:
            argsorted = np.argsort(nn_pred, axis=0)[::-1]
            nn_pred_idx = np.vstack([argsorted[:num_neighbors], argsorted[-num_neighbors:]])
            colnames = ['neighbor ' + str(i) for i in range(num_neighbors)] + ['neighbor ' + str(i) for i in range(-num_neighbors, 0)]
    else:
        logging.info('computing analogies using linewise additive method')
        nn_pred_idx = np.zeros(l, dtype=np.int32)
        for i in range(l):
            nn_pred = cos(vectors.vectors, target_vecs[i]).reshape(1, -1).squeeze()
            nn_pred_idx[i] = np.argmax(nn_pred)

    # return pandas df with nearest neighbors
    results = vectors.words[nn_pred_idx]
    neighbors = pd.DataFrame(np.hstack([target_labels.reshape(-1, 1), results.T]), columns=['target'] + colnames)

    return neighbors


def find_nn(vecs_fname, items_fname, num_neighbors=-1, whole_matrix=False, items_are_vecs=True):
    """Solve novel analogies, using word vectors.

    Writes predictions to tab-separated text file.

    :param vecs_fname: file containing word vectors to use for prediction.
    :param analogies_fname: file containing analogies in tab-separated columns named 'a1', 'a2', and 'b1'
    :param method: solving method to use (options are `additive` and `multiplicative`, multiplicative is the default and usually performs best)
    :param whole_matrix: boolean determining whether to use whole matrix multiplication (faster, but uses more RAM than you may have available, `False` is the default)
    """
    logging.info(f'solving novel analogies with {vecs_fname}')
    vectors = Vectors(vecs_fname, normalize=True, n=3e3, d=300)
    if items_are_vecs:
        #targets = np.loadtxt(items_fname)
        #target_labels = targets[:, 0]
        #target_vecs = targets[:, 1:]
        d = 300
        target_vecs = pca_vecs(vectors.vectors, d)
        target_labels = np.array(list(range(d)))
    else:
        targets = pd.read_csv(items_fname, sep='\t', comment='#')
        target_labels = list(targets['words'])
        target_vecs = None
    neighbors = compute_nn(vectors, target_vecs=target_vecs, target_labels=target_labels, num_neighbors=num_neighbors, whole_matrix=whole_matrix)
    base_fname = '.'.join(items_fname.split('.')[:-1])
    neighbors.to_csv(f'{base_fname}.neighbors.tsv', sep='\t', index=False)


def pca_vecs(target_vecs, d=300):
    pca = sklearn.decomposition.PCA(d)
    components = pca.fit(target_vecs).components_
    return components


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='find nearest neighbors for words or vectors')
    argparser.add_argument('vecs_fname', help='word vectors to use')
    argparser.add_argument('items_fname', help='file containing words or vectors to find nearest neighbors for')
    argparser.add_argument('num_neighbors', type=int, help='number of neighbors to retrieve')
    argparser.add_argument('--whole_matrix', action='store_true',
                           help='perform computations using whole matrices instead of column-wise (potentially results in big memory footprint)')
    args = argparser.parse_args()

    find_nn(**vars(args))
