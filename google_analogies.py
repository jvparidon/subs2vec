# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
from scipy.spatial.distance import cdist
from utensilities import timer
from vecs import load_vecs, print_result


def get_analogies(analogies_set, subsets=False):
    if analogies_set == 'syntactic':
        fname = '../google_analogies/syntactic.txt'
    elif analogies_set == 'semantic':
        fname = '../google_analogies/semantic.txt'
    with open(fname, 'r') as analogies_file:
        if subsets:
            analogies = {}
            for line in analogies_file:
                if line[0] == ':':
                    subset = line.lower().strip('\n')
                    analogies[subset] = []
                else:
                    analogies[subset].append(line.lower().strip('\n').split(' '))
        else:
            analogies = [line.lower().strip('\n').split(' ') for line in analogies_file if line[0] != ':']
    return analogies


@timer
def solve_analogies(analogies, vecs_dict, method='additive', whole_matrix=False):
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

    # normalize to unit length
    '''
    vecs = vecs / np.linalg.norm(vecs, axis=1).reshape(-1, 1)
    a1 = a1 / np.linalg.norm(a1, axis=1).reshape(-1, 1)
    a2 = a2 / np.linalg.norm(a2, axis=1).reshape(-1, 1)
    b1 = b1 / np.linalg.norm(b1, axis=1).reshape(-1, 1)
    '''
    #print('vecs and analogies stacked, computing cosine distances')


    def cos(a, b):
        return np.matmul(a, b.T)


    # compute cosine distance between all word vecs and
    # the vecs predicted from the word word analogy arrays
    if method == 'multiplicative':
        # multiplicative method from Levy & Goldberg (2014)
        eps = np.finfo(np.float64).eps
        if whole_matrix:
            cos_a1 = (1.0 + cos(vecs, a1)) / 2.0
            cos_a2 = (1.0 + cos(vecs, a2)) / 2.0
            cos_b1 = (1.0 + cos(vecs, b1)) / 2.0
            b2_predictions = (cos_b1 * cos_a2) / (cos_a1 + eps)
        else:
            b2_predictions = np.zeros((vecs.shape[0], b1.shape[0]))
            for i in range(b1.shape[0]):
                cos_a1 = (1.0 + cos(vecs, a1[i].reshape(1, -1))) / 2.0
                cos_a2 = (1.0 + cos(vecs, a2[i].reshape(1, -1))) / 2.0
                cos_b1 = (1.0 + cos(vecs, b1[i].reshape(1, -1))) / 2.0
                b2_predictions[:, i] = ((cos_b1 * cos_a2) / (cos_a1 + eps)).squeeze()

    elif method == 'additive':
        # additive method from Mikolov et al. (2013)
        if whole_matrix:
            b2_predictions = cos(vecs, b1 - a1 + a2)
        else:
            b2_predictions = np.zeros((vecs.shape[0], b1.shape[0]))
            for i in range(b1.shape[0]):
                b2_predictions[:, i] = cos(vecs, (b1[i] - a1[i] + a2[i]).reshape(1, -1)).squeeze()

    #print('computed predicted vecs matrix of dimensions {}'.format(b2_predictions.shape))
    #print('computed cosine distances, matching predicted vecs to words')

    # zero out b1s
    b1_idx = np.in1d(words, b1_words)
    b2_predictions[b1_idx] = -1.0

    b2_maxidx = np.argmax(b2_predictions, axis=0)
    b2_predicted_words = words[b2_maxidx]

    return np.mean(b2_predicted_words == b2_targets), total - missing, total


def evaluate_vecs(vecs_dict,
                  verbose=True,
                  analogies_types=['syntactic', 'semantic'],
                  methods=['additive', 'multiplicative'],
                  subsets=False):
    results = []
    for analogies_type in analogies_types:
        analogies = get_analogies(analogies_type, subsets)
        for method in methods:
            if subsets:
                for subset in sorted(analogies.keys()):
                    result, t = solve_analogies(analogies[subset], vecs_dict, method=method)
                    label = '{} ({})'.format(subset[2:], method)
                    if verbose:
                        print_result(label, result, t['duration'])
                    results.append((label, result, t['duration']))
            else:
                results.append('{} ({})'.format(analogies_type, method), solve_analogies(analogies, vecs_dict, method=method)[0])
    if verbose:
        #[print('{: <50}{:0.2f}'.format(*entry)) for entry in results]
        pass
    return results


if __name__ == '__main__':
    #vecs_fname = '../word2phrase/dedup.en.5pass.d5.t100.neg10.epoch10.vec'
    vecs_fname = '../pretrained_reference/fasttext/wiki-news-300d-1M-subword.vec'
    vecs_dict = load_vecs(vecs_fname, normalize=True)
    '''
    analogies_types = ['syntactic', 'semantic']
    methods = ['additive', 'multiplicative']
    for analogies_type in analogies_types:
        analogies = get_analogies(analogies_type)
        print('solving analogies of type: {}'.format(analogies_type))
        #analogies = analogies[6000:7000]
        #analogies = analogies[0:1000]
        for method in methods:
            results, t = solve_analogies(analogies, vecs_dict, method=method, whole_matrix=False)
            print('correctly solved {:0.2f}% of analogies in {} seconds using method {}'.format(results * 100, int(t['duration']), method))
    '''
    evaluate_vecs(vecs_dict, subsets=True)
