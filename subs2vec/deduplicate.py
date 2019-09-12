"""Remove duplicate lines from a text file."""
import os
import argparse
import random
import itertools
from .utensils import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


@log_timer
def dedup_file(in_fname, out_fname):
    """Removes duplicate lines from a text file.

    Writes directly to text file.

    :param in_fname: file to read text from
    :param out_fname: file to write text to
    """
    with open(in_fname, 'r') as in_file, open(out_fname, 'w') as out_file:
        lines = in_file.read().split('\n')
        n_lines = len(lines)
        lines = list(set(lines))
        n_duplicates = n_lines - len(lines)
        random.shuffle(lines)
        out_file.write('\n'.join(lines))
    logging.info(f'deduplicated {in_fname}, removed {n_duplicates} duplicates out of {n_lines} lines')
    return n_lines, n_duplicates


@log_timer
def big_dedup_file(in_fname, out_fname, n_bins):
    """Remove duplicate lines from a text file that does not fit into RAM.

    Because of `itertools.cycle()` this is only pseudorandomized and pseudodeduplicated
    (i.e.: consecutive lines of input cannot end up as consecutive in the output and up to n_bins duplicates of an item may remain).
    If your file fits into RAM afterward, you may consider running it through normal deduplication (which includes true randomization).
    Writes directly to text file.

    :param in_fname: file to read text from
    :param out_fname: file to write text to
    :param n_bins: number of bins to split files into (note that up to n_bins duplicates of any given line may remain after applying this function.
    """
    filehandles = []
    for i in range(n_bins):
        filehandles.append(open(f'temp{i}.txt', 'w'))
    handle_iter = itertools.cycle(filehandles)
    with open(in_fname, 'r') as in_file:
        for line in in_file:
            next(handle_iter).write(line)
    for filehandle in filehandles:
        filehandle.close()

    with open(out_fname, 'w') as out_file:
        for i in range(n_bins):
            with open(f'temp{i}.txt', 'r') as tempfile:
                # deduplicate
                lines = list(set(tempfile.read().split('\n')))
                random.shuffle(lines)
                out_file.write('\n'.join(lines))
    logging.info(f'pseudodeduplicated {in_fname}, {out_fname} is also pseudorandomized')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='remove duplicate lines from a text file')
    argparser.add_argument('fname', help='file to deduplicate')
    argparser.add_argument('--bins', default=1, type=int,
                           help='number of temporary files to use when the input file is too big to fit in memory')
    args = argparser.parse_args()

    path, fname = os.path.split(args.fname)
    if args.bins == 1:
        dedup_file(in_fname=args.fname, out_fname=os.path.join(path, 'dedup.' + fname))
    else:
        big_dedup_file(in_fname=args.fname, out_fname=os.path.join(path, 'dedup.' + fname), n_bins=args.bins)
