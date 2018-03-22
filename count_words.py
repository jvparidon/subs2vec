# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os


def count_words(filename):
    with open(filename, 'r') as infile:
        wordcount = 0
        for line in infile:
            wordcount += len(line.split())
        return wordcount


if __name__ == '__main__':
    folder = 'OpenSubtitles2018/raw'
    for filename in os.listdir(folder):
        if filename.endswith('.txt'):
            wordcount = count_words(os.path.join(folder, filename))
            print('{}M words in file {}'.format(int(wordcount / 1000000), filename))
