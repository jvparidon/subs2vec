"""Download datasets for training subs2vec models (not Windows-compatible)."""
import subprocess
import os
import argparse


def download(lang, corpus):
    """Convenient method for downloading corpora.

    Uses the subprocess module and curl to download corpora.
    Downloads to `corpora/`. Not Windows-compatible.

    :param lang: language to download (use 2-letter ISO code)
    :param corpus: corpus to download, (options are `subs` or `wiki`)
    """
    urls = {
        'subs': f'http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/raw/{lang}.zip',
        'wiki': f'https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/{lang}wiki/20190401/{lang}wiki-20190401-pages-meta-current.xml.bz2'
    }
    subprocess.run(['curl', '-OLk', urls[corpus]])


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='download datasets for training subs2vec models (not Windows-compatible)')
    argparser.add_argument('lang', help='language to download (use 2-letter ISO code)')
    argparser.add_argument('corpus', choices=['subs', 'wiki'], help='corpus to download')
    args = argparser.parse_args()

    download(**vars(args))
