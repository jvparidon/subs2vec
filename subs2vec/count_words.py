"""Count words in a training corpus or other file or directory of files."""
import os
import argparse


def count_words(fname):
    """Count words in a file.

    :param fname: name of file to count words in
    :return: number of words in the file
    """
    with open(fname, 'r') as infile:
        wordcount = 0
        linecount = 0
        for line in infile:
            line = line.strip('\n')
            if line != '':
                linecount += 1
                wordcount += len(line.split(' '))
        return wordcount, linecount


def count_words_in_path(path):
    """Count words in text files on a given path.

    :param path: either filename or directory name to count words in
    """
    print('file\twords\tlines\tmean_line_length')
    if os.path.isdir(path):
        for fname in sorted(os.listdir(path)):
            if fname.endswith('.txt'):
                filepath = os.path.join(path, fname)
                wordcount, linecount = count_words(filepath)
                print(f'{fname}\t{wordcount}\t{linecount}\t{wordcount / linecount}')
    else:
        wordcount, linecount = count_words(path)
        print(f'{path}\t{wordcount}\t{linecount}\t{wordcount / linecount:.2f}')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='count words in text files')
    argparser.add_argument('path', help='file or directory that files are located in')
    args = argparser.parse_args()

    count_words_in_path(args.path)
