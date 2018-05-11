# -*- coding: utf-8 -*-
# jvparidon@gmail.com
"""Tool for stripping XML tags from subtitle corpus. Runs fastest when parallelized on the MPI cluster."""
import os
import argparse
import gzip
import io
import codecs
import numpy as np
from lxml import etree
from joblib import Parallel, delayed
from utensilities import timer
from multiprocessing import cpu_count
cores = int(cpu_count() / 2)


def strip_upos(tree):
    # format [word]_[POS tag]
    stripped = []
    for node in tree.iter():
        if node.tag == 's':
            stripped.append('\n')
        if node.tag == 'w':
            stripped.append(u'{}_{} '.format(node.text, node.get('upos')))
    return u''.join(stripped)


def strip_lemma(tree):
    # format [lemmatized word]
    stripped = []
    for node in tree.iter():
        if node.tag == 's':
            stripped.append('\n')
        if node.tag == 'w':
            stripped.append(u'{} '.format(node.get('lemma')))
    return u''.join(stripped)


def strip_txt(tree):
    # format [sentence]
    for node in tree.iter():
        if node.tag == 'meta':
            tree.remove(node)
    return etree.tostring(tree, encoding='unicode', method='text')


def strip_viz(tree):
    # format [timestamp in ms] [sentence]
    stripped = []
    for node in tree.iter():
        if node.tag == 's':
            children = list(node)
            if len(children) > 0:
                if children[0].tag == 'time':
                    timestamp = children[0].get('value').replace(':', '').replace(',', '.')
                    stripped.append(u'{} {}'.format(timestamp, etree.tostring(node, encoding='unicode', method='text').replace('\n', '')))
    return u'\n'.join(stripped)


xmlparser = etree.XMLParser(recover=True, encoding='utf-8')  # recover option is needed to deal with malformed XML in subs
def strip_xml(text, ioformat='txt'):
    tree = etree.fromstring(text, xmlparser)
    if ioformat == 'upos':
        return strip_upos(tree)
    elif ioformat == 'lemma':
        return strip_lemma(tree)
    elif ioformat == 'txt':
        return strip_txt(tree)
    elif ioformat == 'viz':
        return strip_viz(tree)


def strip_folder(folder, ioformat='txt'):
    filepaths = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.xml.gz'):
                filepaths.append(os.path.join(root, filename))
    for filepath in sorted(filepaths):
        with gzip.open(filepath, 'rb') as infile, io.open(filepath.replace('.xml.gz', '.{}'.format(ioformat)), 'w', encoding='utf-8') as outfile:
            outfile.write(strip_xml(infile.read(), ioformat))
    return len(filepaths)


@timer
def strip_parallelized(folder, lang, ioformat='txt', cores=1):
    return Parallel(n_jobs=cores)(delayed(strip_folder)(os.path.join(folder, lang, year), ioformat) for year in sorted(os.listdir(os.path.join(folder, lang))))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='join xml-stripped subs into a single training file for word2vec-style models')
    argparser.add_argument('--directory', default=None, help='folder where the files are located')
    argparser.add_argument('--ioformat', default='txt', choices=['txt', 'lemma', 'upos', 'viz'], help='input/output format')
    args = argparser.parse_args()

    ioformat = args.ioformat
    folder = args.directory
    if folder is None:
        folder = '../OpenSubtitles2018/parsed' if (ioformat in ['upos', 'lemma']) else '../OpenSubtitles2018/raw'
    for lang in sorted(os.listdir(folder)):
        if '.' not in lang:
            results, t = strip_parallelized(folder, lang, ioformat=ioformat, cores=cores)
            print('stripped xml from {} {} files in {} seconds'.format(np.sum(results), lang, int(t['duration'])))
