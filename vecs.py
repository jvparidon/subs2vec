# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import argparse
import faruqui_measures
import google_analogies
import response_times


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


def evaluate_vecs(vecs_dict, lang='en', dissimilarities=True, rts=True, analogies=True):
    if lang == 'en':
        if dissimilarities:
            faruqui_measures.evaluate_vecs(vecs_dict, verbose=True)
        if rts:
            response_times.evaluate_vecs(vecs_dict, verbose=True)
    if analogies:
        google_analogies.evaluate_vecs(vecs_dict, lang, verbose=True)


if __name__ == '__main__':
    default_fname = '../pretrained/fasttext/wiki-news-300d-1M-subword.vec'

    argparser = argparse.ArgumentParser(description='evaluate a set of word embeddings')
    argparser.add_argument('--filename', default=default_fname,
                           help='word vectors to evaluate')
    argparser.add_argument('--lang', default='en', choices=['en', 'fr', 'hi', 'pl'],
                           help='language to solve analogies in (uses ISO 3166-1 codes)')
    argparser.add_argument('--dissimilarities', default=True, type=bool,
                           help='Faruqui semantic dissimilarity correlations')
    argparser.add_argument('--rts', default=True, type=bool,
                           help='Semantic Priming Project response time predictions')
    argparser.add_argument('--analogies', default=True, type=bool,
                           help='Google (Mikolov) analogy problems')
    args = argparser.parse_args()

    # bypass filename from argparse for convenient testing of multiple files
    fnames = ['../tmp-jeroen/en.dedup.5pass.d5.t100.vec',
              '../pretrained/fasttext/wiki-news-300d-1M-subword.vec',
              '../pretrained/mkb2017.vec',
              '../pretrained/fasttext/crawl-300d-2M.vec',
              '../reddit/reddit.dedup.sg.lr01.vec']
    fnames = ['../tmp-jeroen/en.dedup.5pass.d5.t100.3000d.vec']
    fnames = ['../tmp-jeroen/bn.dedup.utf-8.5pass.d5.t100.neg5.epoch5.t0.0001.300d.vec']
    for fname in fnames:
        vecs_dict = load_vecs(fname, n=1e6, normalize=True, d=300)
        evaluate_vecs(vecs_dict,
                      lang=args.lang,
                      dissimilarities=args.dissimilarities,
                      rts=args.rts,
                      analogies=args.analogies)
