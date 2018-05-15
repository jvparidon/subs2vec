# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
from scipy.spatial.distance import cosine


def load_vecs(filename, normalize=False, dims=300):
    def normalize_vec(x):
        return x / np.linalg.norm(x)
    print('loading vecs: {}'.format(filename))
    vecs_dict = {}
    with open(filename, 'r', encoding='latin-1') as vecfile:
        for line in vecfile:
            line = line.split(' ')
            if len(line) > dims:
                if normalize:
                    vecs_dict[line[0]] = normalize_vec(np.array([float(num) for num in line[1:dims + 1]]))
                else:
                    vecs_dict[line[0]] = np.array([float(num) for num in line[1:dims + 1]])
    return vecs_dict


def print_result(label, result, t=0):
    if t > 0:
        print('{: <50}{:0.2f} ({: >5}/{: >5}) in {}s'.format(label, *result, int(t)))
    else:
        print('{: <50}{:0.2f} ({: >5}/{: >5})'.format(label, *result))
