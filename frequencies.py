import argparse
from collections import Counter


def count_freqs(filename):
    word_count = 0
    line_count = 0
    freq_counter = Counter()
    with open(filename, 'r') as in_file:
        for line in in_file:
            line = line.strip('\n').split(' ')
            line_count += 1
            word_count += len(line)
            freq_counter.update(line)
    return freq_counter, word_count, line_count


def write_freqs(filename, freq_counter, word_count):
    with open(filename, 'w') as out_file:
        out_file.write('word\tcount\tfreq\n')
        for entry in freq_counter.most_common():
            out_file.write(f'{entry[0]}\t{entry[1]}\t{entry[1] / word_count}\n')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='count word frequencies')
    argparser.add_argument('--filename', help='text file to count from')
    args = argparser.parse_args()

    freq_counter, word_count, _ = count_freqs(args.filename)
    print(f'counted {word_count} words in total')
    write_freqs(f'{args.filename}_freqs', freq_counter, word_count)