"""Count words in a training corpus or other file or directory of files."""
import os
import argparse


def count_words(filename):
    """Count words in a file.

    :param filename: name of file to count words in
    :return: number of words in the file
    """
    with open(filename, 'r') as infile:
        wordcount = 0
        for line in infile:
            line = line.strip('\n')
            if line != '':
                wordcount += len(line.split(' '))
        return wordcount


def print_count(wordcount, filename):
    """Print the number of words in a file to the command line.

    Formats numbers for legibility, prints directly to command line.

    :param wordcount: number of words to format
    :param filename: filename to display
    """
    if wordcount > 10000000000:
        print('{: >6}B words in file {}'.format(int(wordcount / 1000000000), filename))
    elif wordcount > 10000000:
        print('{: >6}M words in file {}'.format(int(wordcount / 1000000), filename))
    elif wordcount > 10000:
        print('{: >6}K words in file {}'.format(int(wordcount / 1000), filename))
    else:
        print('{: >6}  words in file {}'.format(wordcount, filename))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='count words in files in a given directory')
    argparser.add_argument('filename', help='file or directory that files are located in')
    args = argparser.parse_args()

    if os.path.isdir(args.filename):
        for filename in sorted(os.listdir(args.filename)):
            if filename.endswith('.txt'):
                filepath = os.path.join(args.filename, filename)
                wordcount = count_words(filepath)
                print_count(wordcount, filepath)
    else:
        wordcount = count_words(args.filename)
        print_count(wordcount, args.filename)
