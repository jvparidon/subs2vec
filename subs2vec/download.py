# -*- coding: utf-8 -*-
# jvparidon@gmail.com
"""Download datasets for training subs2vec models (not Windows-compatible)."""
import subprocess
import os
import argparse


def download(lang, corpus):
    """Convenient method for downloading corpora.

    Uses the subprocess module and curl to download corpora.
    Downloads to `corpora/`. Not Windows-compatible.

    :param lang: Language to download (use 2-letter ISO code)
    :param corpus: Corpus to download
    """
    urls = {
        'sub': f'http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/parsed/{lang}.zip',
        'wiki': f'https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/{lang}wiki/20190401/{lang}wiki-20190401-pages-meta-current.xml.bz2'
    }
    subprocess.run(['curl', '-OLk', urls[corpus]])


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='download datasets for training subs2vec models (not Windows-compatible)')
    argparser.add_argument('lang', help='anguage to download (use 2-letter ISO code)')
    argparser.add_argument('corpus', choices=['sub', 'wiki'], help='corpus to download')
    args = argparser.parse_args()

    # check if corpora dir exists, otherwise make it
    if not os.path.isdir('corpora'):
        os.mkdir('corpora')

    # change to corpora dir and download user-specified corpus
    os.chdir('corpora')
    download(args.lang, args.corpus)
