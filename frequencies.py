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
