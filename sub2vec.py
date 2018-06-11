# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
import argparse
import numpy as np
import subprocess as sp
import strip_subs
import join_subs
import deduplicate
from utensilities import timer
from multiprocessing import cpu_count


@timer
def train_fasttext(training_data, working_dir, cores, dim=300):
    base_fname = training_data.strip('.txt')
    binary = ['../local-bin/fasttext']
    method = ['skipgram']
    train = ['-input', training_data]
    output = ['-output', os.path.join(working_dir,
                                      training_data.split('/')[-1]
                                      .replace('.txt', ''))]
    neg = ['-neg', str(5)]
    epoch = ['-epoch', str(5)]
    t = ['-t', str(.0001)]
    dim = ['-dim', str(dim)]
    thread = ['-thread', str(cores)]
    sp.run(binary + method + train + output + neg + epoch + t + dim + thread)
    model = '{}.bin'.format(base_fname)
    vecs = '{}.vec'.format(base_fname)
    return model, vecs


@timer
def build_phrases(training_data, working_dir, phrase_pass):
    base_fname = os.path.join(working_dir,
                              training_data.split('/')[-1].replace('.txt', ''))
    for i in range(phrase_pass):
        t = (2 ** (phrase_pass - i - 1)) * 100
        output_fname = '{}.{}pass.d5.t{}.txt'.format(base_fname, i + 1, t)
        binary = ['../local-bin/word2phrase']
        train = ['-train', training_data]
        output = ['-output', output_fname]
        d = ['-min-count', str(5)]
        t = ['-threshold', str(t)]
        sp.run(binary + train + output + d + t)
        training_data = output_fname
    return training_data


@timer
def generate(lang, working_dir, subs_dir, subs_prep, dedup, phrase_pass, cores):
    if lang == 'all':
        langs = sorted(os.listdir(os.path.join(subs_dir, 'raw')))
    else:
        langs = [lang]
    for lang in langs:
        # prep subs
        if subs_prep:
            training_data = os.path.join(subs_dir, 'raw')
            # strip subs
            print('stripping xml from subs in language {}'.format(lang))
            results, t = strip_subs.strip_parallelized(training_data, lang,
                                                       ioformat='txt',
                                                       cores=cores)
            print('stripped xml from {} files in {} seconds'
                  .format(np.sum(results), int(t['duration'])))
            # join subs
            print('concatenating training data for language {}'.format(lang))
            results, t = join_subs.join_dir(training_data, working_dir, lang,
                                            verbose=True, ioformat='txt')
            print('concatenated {} files in {} seconds'
                  .format(results, int(t['duration'])))

        training_data = os.path.join(working_dir, '{}.txt'.format(lang))

        # deduplicate
        if dedup:
            print('deduplicating {}'.format(training_data))
            out_fname = os.path.join(working_dir,
                                     training_data.split('/')[-1]
                                     .replace('.txt', '.dedup.txt'))
            results, t = deduplicate.dedup_file(training_data, out_fname)
            n_lines, n_duplicates = results
            training_data = out_fname
            print('read {} lines and removed {} duplicates in {} seconds'
                  .format(n_lines, n_duplicates, int(t['duration'])))

        # build phrases
        print('building phrases for {}'.format(training_data))
        training_data, t = build_phrases(training_data, working_dir,
                                         phrase_pass)
        print('built phrases in {} passes in {} seconds'
              .format(phrase_pass, int(t['duration'])))

        # train fastText model
        results, t = train_fasttext(training_data, working_dir, cores)
        model, vecs = results
        print('trained fastText model in {} seconds'.format(int(t['duration'])))
        print('model binary at {}'.format(model))
        print('word vectors at {}'.format(vecs))

    return langs


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='generate a fastText model from OpenSubtitles data')
    argparser.add_argument('--working_dir', default='../tmp-jeroen',
        help='working directory, write permission required')
    argparser.add_argument('--lang', default='en',
        help='source language (OpenSubtitles data uses ISO 3166-1 codes)')
    argparser.add_argument('--subs_dir', default='../OpenSubtitles2018',
        help='location of OpenSubtitles data')
    argparser.add_argument('--subs_prep', default=False, type=bool,
        help='xml-strip and concatenate subs (true/false)')
    argparser.add_argument('--dedup', default=True, type=bool,
        help='deduplicate training data line-wise (true/false)')
    argparser.add_argument('--phrase_pass', default='5', type=int,
        help='number of phrase-building passes, 0 equals no phrase-building')
    argparser.add_argument('--cores', default=int(cpu_count() / 2), type=int,
        help='number of cores to use for the parts that can be parallelized')
    args = argparser.parse_args()

    lang, t = generate(**vars(args))
    print('generated sub2vec model for language {} in {} seconds'
          .format(lang, int(t['duration'])))
