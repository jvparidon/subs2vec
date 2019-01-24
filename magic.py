# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import argparse
from utensilities import timer
import vecs


def get_analogies():
    analogies = [['dog', 'small'],
                 ['dog', 'young'],
                 ['puppy', 'dog'],
                 ['dog', 'puppy'],
                 ['cat', 'small'],
                 ['cat', 'young'],
                 ['kitten', 'cat'],
                 ['cat', 'kitten'],
                 ['push', 'shove'],
                 ['shove', 'push'],
                 ['push', 'hard'],
                 ['hard', 'push'],
                 ['wild', 'dog'],
                 ['dog', 'wild'],
                 ['wild', 'pig'],
                 ['wild', 'cow'],
                 ['big', 'house'],
                 ['small', 'apartment'],
                 ['tall', 'tree']]
    return analogies


@timer
def solve_analogies(analogies, vecs_dict, method='additive', whole_matrix=False):
    missing = 0
    total = len(analogies)
    # make numpy arrays of vecs for given words in analogies
    a = []
    b = []
    b_words = []
    for analogy in analogies:
        if all(word in vecs_dict.keys() for word in analogy):
            a += [vecs_dict[analogy[0]]]
            b += [vecs_dict[analogy[1]]]
            b_words += [analogy[1]]
        else:
            missing += 1
    a = np.vstack(a)
    b = np.vstack(b)
    b_words = np.vstack(b_words)
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

    if whole_matrix:
        if method == 'additive':
            b2_predictions = cos(vecs, a + b)
        elif method == 'addition':
            b2_predictions = cos(vecs, a) + cos(vecs, b)
        elif method == 'subtractive':
            b2_predictions = cos(vecs, a - b)
        elif method == 'subtraction':
            b2_predictions = cos(vecs, a) - cos(vecs, b)
        elif method == 'mean':
            b2_predictions = cos(vecs, (a + b) / 2.0)
        elif method == 'geom_mean':
            b2_predictions = cos(vecs, np.sqrt((np.square(a) + np.square(b)) / 2.0))
        elif method == 'multiplication':
            b2_predictions = cos(vecs, a) * cos(vecs, b)
        elif method == 'division':
            b2_predictions = cos(vecs, a) / (cos(vecs, b) + 1e-8)
        # zero out b1s (yes, this feels like cheating)
        for i in range(len(analogies)):
            b2_predictions[np.isin(words.squeeze(), analogies[i])] = -1.0
        b2_predicted_idx = np.argmax(b2_predictions, axis=0)
    else:
        b2_predicted_idx = np.zeros(b1.shape[0], dtype=np.int32)
        for i in range(b1.shape[0]):
            b2_prediction = cos(vecs, (b1[i] - a1[i] + a2[i]).reshape(1, -1)).squeeze()
            # zero out b1s (yes, this feels like cheating)
            #b2_prediction[np.where(words == b1_words[i])[0]] = -1.0
            b2_prediction[np.isin(words.squeeze(), analogies[i])] = -1.0
            b2_predicted_idx[i] = np.argmax(b2_prediction)

    b2_predicted_words = words[b2_predicted_idx]
    print('\n{}'.format(method))
    [print('{} {}'.format(analogies[i], b2_predicted_words[i])) for i in range(len(analogies))]
    return True


def evaluate_vecs(vecs_dict,
                  verbose=True,
                  methods=['additive', 'subtractive', 'mean', 'geom_mean', 'multiplication', 'division', 'addition', 'subtraction'],
                  whole_matrix=False):
    analogies = get_analogies()
    for method in methods:
        result, t = solve_analogies(analogies, vecs_dict, method=method, whole_matrix=whole_matrix)
    return True


if __name__ == '__main__':
    #vecs_fname = '../tmp-jeroen/en.dedup.5pass.d5.t100.vec'
    #vecs_fname = '../pretrained_reference/mkb2017.vec'
    #vecs_fname = '../pretrained_reference/fasttext/crawl-300d-2M.vec'
    vecs_fname = '../pretrained_reference/fasttext/wiki-news-300d-1M-subword.vec'

    argparser = argparse.ArgumentParser(description='solve syntactic and semantic analogies from Mikolov et al. (2013)')
    argparser.add_argument('--filename', default=vecs_fname, help='word vectors to evaluate')
    argparser.add_argument('--whole_matrix', default=True, help='perform computations using whole matrices instead of column-wise (potentially results in massive memory use)')
    args = argparser.parse_args()

    vecs_dict = vecs.load_vecs(args.filename, normalize=True)
    results = evaluate_vecs(vecs_dict, whole_matrix=args.whole_matrix)
