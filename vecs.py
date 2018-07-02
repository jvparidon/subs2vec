# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import argparse
import similarities
import analogies


def load_vecs(filename, normalize=False, n=False, d=300):
    def normalize_vec(x):
        return x / np.linalg.norm(x)
    print('loading vecs: {}'.format(filename))
    vecs_dict = {}
    with open(filename, 'r', encoding='utf-8') as vecfile:
        i = 0
        for line in vecfile:
            line = line.split(' ')
            if len(line) > d:
                if normalize:
                    vecs_dict[line[0]] = normalize_vec(np.array([float(num) for num in line[1:d + 1]]))
                else:
                    vecs_dict[line[0]] = np.array([float(num) for num in line[1:d + 1]])
            i += 1
            if n and (i > n):
                return vecs_dict
    return vecs_dict


def print_result(label, result, t=0):
    if t > 0:
        print('{: <50}{: 5.2f} ({: >5}/{: >5}) in {}s'.format(label, *result, int(t)))
    else:
        print('{: <50}{: 5.2f} ({: >5}/{: >5})'.format(label, *result))


def evaluate_vecs(vecs_dict, lang, no_similarities=False, no_analogies=False):
    if no_similarities:
        logging.info('skipping similarities')
    else:
        similarities.evaluate_vecs(vecs_dict, lang, verbose=True)
    if no_analogies:
        logging.info('skipping analogies')
    else:
        analogies.evaluate_vecs(vecs_dict, lang, verbose=True)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='evaluate a set of word embeddings')
    argparser.add_argument('--filename',
                           help='word vectors to evaluate')
    argparser.add_argument('--lang',
                           help='language to evaluate vector in (use ISO 639-1 codes)')
    argparser.add_argument('--no_similarities', action='store_true',
                           help='do not include semantic similarity correlations')
    argparser.add_argument('--no_analogies', action='store_true',
                           help='do not include analogy problems')
    args = argparser.parse_args()

    vecs_dict = load_vecs(args.filename, n=1e6, normalize=True)
    evaluate_vecs(vecs_dict,
                  lang=args.lang,
                  no_similarities=args.no_similarities,
                  no_analogies=args.no_analogies)
