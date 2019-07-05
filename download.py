# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import subprocess
import os


def download(lang, source):
    if source == 'subs':
        subprocess.run(['curl', '-OLk', f'http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/parsed/{lang}.zip'])
    elif source == 'wiki':
        subprocess.run(['curl', '-OLk', f'https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/{lang}wiki/20190301/{lang}wiki-20190301-pages-articles.xml.bz2'])
    elif source == 'wiki-meta':
        subprocess.run(['curl', '-OLk', f'https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/{lang}wiki/20190401/{lang}wiki-20190401-pages-meta-current.xml.bz2'])


if __name__ == '__main__':
    langs = sorted(os.listdir('../for_publication/'))
    os.chdir('../data/wiki-meta-new')
    for lang in langs:
        if not os.path.isdir(lang):
            os.mkdir(lang)
        os.chdir(lang)
        print(f'downloading {lang}')
        download(lang, 'wiki-meta')
        os.chdir('../')
