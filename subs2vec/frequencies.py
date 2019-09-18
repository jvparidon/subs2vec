"""Extract unigram, bigram, and trigram frequencies, either from a text corpus or from a pre-existing frequencies file."""
import argparse
import collections
import os
import pandas as pd
from .utensils import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


@log_timer
def count_ngrams(fname, kind='words', min_freq=1, no_bigrams=False, no_trigrams=False):
    """Counts unigrams, bigrams, and trigrams line-by-line in a text corpus.

    :param fname: text corpus to count in
    :param kind: kind of items to count (options are 'words' or 'letters')
    :param min_freq: minimum frequency threshold for an item to be included in the output
    :param no_bigrams: whether to skip counting bigrams for improved speed/memory footprint (default False)
    :param no_trigrams: whether to skip counting trigrams for improved speed/memory footprint (default False)
    :return: tuple of pandas DataFrames containing frequencies for unigrams, bigrams, and trigrams, respectively
    """
    # initialize Counter objects
    unigrams = collections.Counter()
    bigrams = collections.Counter()
    trigrams = collections.Counter()

    # function to update all three counters at once
    def update_counters(item):
        unigrams.update(item)
        if not no_bigrams:
            bigrams.update([' '.join(bigram) for bigram in zip(item[:-1], item[1:])])
        if not no_trigrams:
            trigrams.update([' '.join(trigram) for trigram in zip(item[:-2], item[1:-1], item[2:])])

    # open corpus file and count
    with open(fname, 'r') as txtfile:
        for line in txtfile:
            line = line.lower().strip('\n').split(' ')
            if kind == 'words':
                update_counters(line)
            elif kind == 'letters':
                for word in line:
                    update_counters(list(word))

    # remove items below frequency threshold
    if min_freq > 1:
        for counter in [unigrams, bigrams, trigrams]:
            for key, value in list(counter.items()):
                if value < min_freq:
                    del counter[key]

    # convert to pandas DataFrames and sort
    unigrams = pd.DataFrame.from_dict(unigrams, orient='index', columns=['unigram_freq']).sort_values(by=['unigram_freq'], ascending=False)
    bigrams = pd.DataFrame.from_dict(bigrams, orient='index', columns=['bigram_freq']).sort_values(by=['bigram_freq'], ascending=False)
    trigrams = pd.DataFrame.from_dict(trigrams, orient='index', columns=['trigram_freq']).sort_values(by=['trigram_freq'], ascending=False)

    base_fname = '.'.join(os.path.basename(fname).split('.')[:-1])
    unigrams.to_csv(f'{base_fname}.{kind}.unigrams.tsv', index_label='unigram', sep='\t')
    bigrams.to_csv(f'{base_fname}.{kind}.bigrams.tsv', index_label='bigram', sep='\t')
    trigrams.to_csv(f'{base_fname}.{kind}.trigrams.tsv', index_label='trigram', sep='\t')
    return unigrams, bigrams, trigrams


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Extract unigram, bigram, and trigram frequencies from a text file')
    argparser.add_argument('fname', help='text file to counts frequencies in')
    argparser.add_argument('--kind', default='words', choices=['words', 'letters'])
    argparser.add_argument('--min_freq', help='minimum frequency for an item to be included', default=1, type=int)
    argparser.add_argument('--no_bigrams', help='do not count bigrams', action='store_true')
    argparser.add_argument('--no_trigrams', help='do not count trigrams', action='store_true')
    args = argparser.parse_args()

    count_ngrams(**vars(args))
