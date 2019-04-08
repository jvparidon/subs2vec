# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
import argparse

def count_words(filename):
    with open(filename, 'r') as infile:
        wordcount = 0
        for line in infile:
            line = line.strip('\n')
            if line != '':
                wordcount += len(line.split(' '))
        return wordcount

def print_count(wordcount, filename):
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
    argparser.add_argument('--directory', default='../OpenSubtitles2018/raw', help='directory the files are located in')
    argparser.add_argument('--filename', help='filename (overrides directory argument)')
    args = argparser.parse_args()

    if args.filename:
        wordcount = count_words(args.filename)
        print_count(wordcount, args.filename)
    else:
        folder = args.directory
        for filename in sorted(os.listdir(folder)):
            if filename.endswith('.txt'):
                wordcount = count_words(os.path.join(folder, filename))
                print_count(wordcount, filename)
