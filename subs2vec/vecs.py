"""Provides Vectors object and methods to load, write, and interact with word vectors."""
import numpy as np
import pandas as pd
from .utensils import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


class Vectors:
    """Creates a Vectors object containing numpy arrays of words and word vectors.
    """
    @log_timer
    def __init__(self, fname, normalize=False, n=1e6, d=300):
        self.n = int(n)
        self.d = d
        logging.info(f'loading vectors {fname}')

        with open(fname, 'r', encoding='utf-8') as vecfile:
            # skip header
            next(vecfile)

            # initialize arrays
            self.vectors = np.zeros((self.n, self.d))
            self.words = np.empty(self.n, dtype=object)

            # fill arrays
            for i, line in enumerate(vecfile):
                if i >= self.n:
                    break
                rowentries = line.rstrip('\n').split(' ')
                self.words[i] = rowentries[0]
                self.vectors[i] = rowentries[1:self.d + 1]

            # truncate empty part of arrays, if necessary
            self.vectors = self.vectors[:i]
            self.words = self.words[:i]
            self.n = i  # reset n to actual array length

            # normalize by L1 norm
            if normalize:
                self.vectors = self.vectors / np.linalg.norm(self.vectors, axis=1).reshape(-1, 1)

    @log_timer
    def as_df(self):
        """Casts word vectors to pandas DataFrame.

        Each row contains a vector, each column corresponds with a vector dimension. Rows are indexed by word.

        :return: pandas DataFrame containing word vectors
        """
        return pd.DataFrame(self.vectors).set_index(self.words)

    @log_timer
    def as_dict(self):
        """Casts word vectors to Python dict.

        The dict is indexed by word, with the items being word vectors in the form of numpy arrays.

        :return: Python dict containing word vectors
        """
        return {self.words[i]: self.vectors[i] for i in range(self.n)}

    @log_timer
    def write_vecs(self, vecs_fname):
        """Writes word vectors to .vec file.

        :param vecs_fname: filename to write vectors to
        """
        header = f'{self.vectors.shape[0]} {self.vectors.shape[1]}'
        np.savetxt(vecs_fname, np.hstack([self.words.reshape(-1, 1), self.vectors]), fmt='%s', header=header)
