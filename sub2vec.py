# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
import argparse
import numpy as np
import subprocess as sp
import strip_subs
import join_subs
import deduplicate
from utensilities import log_timer
import psutil
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
cpu_count = psutil.cpu_count(logical=False)  # logical=False to count only physical cores


@log_timer
def train_fasttext(training_data, prefix, lang, d=300, neg=10, epoch=10, t=.0001):
    model_name = f'{prefix}.{lang}'
    binary = ['fasttext']
    method = ['skipgram']
    train = ['-input', training_data]
    output = ['-output', model_name]
    neg = ['-neg', str(neg)]
    epoch = ['-epoch', str(epoch)]
    t = ['-t', str(t)]
    dim = ['-dim', str(d)]
    thread = ['-thread', str(cpu_count)]
    if logging.getLogger().isEnabledFor(logging.INFO):
        sp.run(binary + method + train + output + neg + epoch + t + dim + thread)
    else:
        sp.run(binary + method + train + output + neg + epoch + t + dim + thread, stdout=sp.DEVNULL)
    model = f'{model_name}.bin'
    vecs = f'{model_name}.vec'
    return model, vecs


@log_timer
def build_phrases(training_data, phrase_pass):
    base_fname = training_data.strip('.txt')
    for i in range(phrase_pass):
        out_fname = f'{base_fname}.{i + 1}pass.d5.t{t}.txt'
        t = (2 ** (phrase_pass - i - 1)) * 100
        binary = ['word2phrase']
        train = ['-train', training_data]
        output = ['-output', out_fname]
        d = ['-min-count', str(5)]
        t = ['-threshold', str(t)]
        if logging.getLogger().isEnabledFor(logging.INFO):
            sp.run(binary + train + output + d + t)
        else:
            sp.run(binary + train + output + d + t, stdout=sp.DEVNULL)
        training_data = out_fname
    return out_fname


def fix_encoding(training_data):
    out_fname = training_data.replace('.txt', '.utf-8.txt')
    with open(training_data, 'r', encoding='utf-8', errors='ignore') as in_file, open(out_fname, 'w', encoding='utf-8') as out_file:
        for line in in_file:
            out_file.write(line)
    return out_fname


@log_timer
def generate(lang, filename, source, prep_data, dedup_data, phrase_pass, years=(1900, 2050)):
    # prep subs
    if prep_data:
        if source in ['subs', 'wiki-sub']:
            training_data = os.path.join(subs_dir, 'raw')
            # strip subs
            logging.info('stripping xml from subs in language {}'.format(lang))
            results, t = strip_subs.strip_parallelized(training_data, lang, ioformat='txt')
            logging.info('stripped xml from {} files in {} seconds'.format(np.sum(results), int(t['duration'])))
            training_data = os.path.join(subs_dir, 'raw')
            # join subs
            logging.info('concatenating training data for language {}'.format(lang))
            results, t = join_subs.join_dir(training_data, './', lang, verbose=True, ioformat='txt', subset_years=subset_years)
            logging.info('concatenated {} files in {} seconds'.format(results, int(t['duration'])))

        training_data = '{}.{}-{}.txt'.format(lang, *years)
        if source in ['wiki', 'wiki-sub']:
            # do wiki prep
            pass
    else:
        training_data = filename

    # deduplicate
    if dedup_data:
        logging.info('deduplicating {}'.format(training_data))
        out_fname = training_data.replace('.txt', '.dedup.txt')
        n_lines, n_duplicates = deduplicate.dedup_file(training_data, out_fname)
        training_data = out_fname

    # build phrases
    logging.info('building phrases for {}'.format(training_data))
    training_data = build_phrases(training_data, phrase_pass)

    # fix potential broken utf-8 encoding
    # logging.info('checking (and fixing) utf-8 encoding for {}'.format(training_data))
    # training_data = fix_encoding(training_data)

    # train fastText model
    logging.info('training fastText model on {}'.format(training_data))
    results = train_fasttext(training_data=training_data, lang=lang, prefix=f'{source}.')
    model, vecs = results
    logging.info('model binary at {}'.format(model))
    logging.info('word vectors at {}'.format(vecs))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='generate a fastText model from OpenSubtitles and Wikipedia data')
    argparser.add_argument('lang',
                           help='source language (OpenSubtitles and Wikipedia data uses ISO 639-1 codes)')
    argparser.add_argument('filename',
                           help='filename if skipping data preparation')
    argparser.add_argument('--source',
                           help='source data, use one of {wiki, sub, wiki-sub} if using automatic data preparation')
    argparser.add_argument('--prep_data', action='store_true')
    argparser.add_argument('--dedup_data', action='store_true',
                           help='deduplicate training data line-wise')
    argparser.add_argument('--phrase_pass', default='5', type=int,
                           help='number of phrase-building passes, 0 equals no phrase-building (default 5)')
    args = argparser.parse_args()

    generate(**vars(args))
