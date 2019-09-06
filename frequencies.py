import argparse
from collections import Counter
from utensilities import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


@log_timer
def count_freqs(filename):
    # add bigram and trigram methods
    n_words = 0
    n_lines = 0
    freq_counter = Counter()
    with open(filename, 'r') as in_file:
        for line in in_file:
            line = line.strip('\n').split(' ')
            n_lines += 1
            n_words += len(line)
            freq_counter.update(line)
    logging.info(f'counted {n_words} words over {n_lines} lines')
    return freq_counter, n_words, n_lines


def write_freqs(filename, freq_counter, n_words, min_freq=1):
    with open(filename, 'w') as out_file:
        out_file.write('item\tcount\tfrequency\n')
        for entry in freq_counter.most_common():
            if entry[1] >= min_freq:
                out_file.write(f'{entry[0]}\t{entry[1]}\t{entry[1] / n_words}\n')


def pull_freqs():
    # pull unigram, bigram, or trigram freqs for a list of words


def pull_n_freqs():


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='count word frequencies')
    argparser.add_argument('--filename', help='text file to counts frequencies in')
    argparser.add_argument('--min_freq', help='minimum frequency for an item to be included', default=1)
    args = argparser.parse_args()

    freq_counter, n_words, _ = count_freqs(args.filename)
    write_freqs(f'{args.filename}_freqs', freq_counter, n_words, args.min_freq)


import pandas as pd
import argparse
import itertools
import collections


def read_txt(filename):
    with open(filename, 'r') as txtfile:
        txt = [tuple(line.split(' '))
               for line in txtfile.read().lower().split('\n')[:-1]]
        txt = set(txt)
    return txt


def count_unigrams(txt):
    unigrams = itertools.chain.from_iterable(txt)
    unigrams = collections.Counter(unigrams)
    return unigrams


def count_bigrams(txt):
    bigrams = itertools.chain.from_iterable([zip(item[:-1], item[1:]) for item in txt])
    bigrams = collections.Counter(bigrams)
    return bigrams


def count_trigrams(txt):
    trigrams = itertools.chain.from_iterable([zip(item[:-2], item[1:-1], item[2:]) for item in txt])
    trigrams = collections.Counter(trigrams)
    return trigrams


# for lower memory consumption, but probably slower (not 100% sure)
def count_ngrams_by_line(filename, kind='words'):
    unigrams = collections.Counter()
    bigrams = collections.Counter()
    trigrams = collections.Counter()
    with open(filename, 'r') as txtfile:
        for line in txtfile:
            line = line.lower().strip('\n').split(' ')

            if kind == 'words':
                unigrams.update(line)
                bigrams.update([' '.join(bigram) for bigram in zip(line[:-1], line[1:])])
                trigrams.update([' '.join(trigram) for trigram in zip(line[:-2], line[1:-1], line[2:])])

            elif kind == 'letters':
                for item in line:
                    item = list(item)
                    unigrams.update(item)
                    bigrams.update([''.join(bigram) for bigram in zip(item[:-1], item[1:])])
                    trigrams.update([''.join(trigram) for trigram in zip(item[:-2], item[1:-1], item[2:])])

    return unigrams, bigrams, trigrams


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Extract unigram and bigram frequencies from a text file')
    argparser.add_argument('--filename')
    argparser.add_argument('--kind', default='words', choices=['words', 'letters'])
    args = argparser.parse_args()

    unigrams, bigrams, trigrams = count_ngrams_by_line(args.filename, args.kind)
    pd.DataFrame.from_dict(unigrams, orient='index', columns=['unigram_freq']).sort_values(by=['unigram_freq'], ascending=False).to_csv(f'{args.kind}_unigram_freqs.tsv', index_label='unigram', sep='\t')
    pd.DataFrame.from_dict(bigrams, orient='index', columns=['bigram_freq']).sort_values(by=['bigram_freq'], ascending=False).to_csv(f'{args.kind}_bigram_freqs.tsv', index_label='bigram', sep='\t')
    pd.DataFrame.from_dict(trigrams, orient='index', columns=['trigram_freq']).sort_values(by=['trigram_freq'], ascending=False).to_csv(f'{args.kind}_trigram_freqs.tsv', index_label='trigram', sep='\t')
