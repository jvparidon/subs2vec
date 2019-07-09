# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import subprocess
import os
import argparse


def download(lang, corpus):
    if corpus == 'sub':
        subprocess.run(['curl', '-OLk', f'http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/parsed/{lang}.zip'])
    elif corpus == 'wiki':
        subprocess.run(['curl', '-OLk', f'https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/{lang}wiki/20190401/{lang}wiki-20190401-pages-meta-current.xml.bz2'])


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='download datasets for training sub2vec models')
    argparser.add_argument('--lang', help='corpus language (use 2-letter ISO code)')
    argparser.add_argument('--corpus', choices=['sub', 'wiki'], help='word vectors to evaluate')
    args = argparser.parse_args()

    if not os.path.isdir('corpora'):
        os.mkdir('corpora')
    os.chdir('corpora')
    download(args.lang, args.corpus)
