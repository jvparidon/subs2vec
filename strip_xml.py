# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import os
import gzip
import codecs
import numpy as np
from lxml import etree
from joblib import Parallel, delayed
from utensilities import timer


parser = etree.XMLParser(recover=True)  # recover option is needed to deal with malformed XML in subs
def strip_xml(text):
    tree = etree.fromstring(text, parser)
    for node in tree.iter():
        if node.tag == 'meta':
            tree.remove(node)
    stripped = etree.tostring(tree, encoding='utf8', method='text')
    return stripped


def strip_folder(folder):
    filepaths = []
    for root, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.xml.gz'):
                filepaths.append(os.path.join(root, filename))
    for filepath in sorted(filepaths):
        with gzip.open(filepath, 'rb') as infile, open(filepath.replace('.xml.gz', '.txt'), 'w') as outfile:
            outfile.write(strip_xml(infile.read()))
    return len(filepaths)


@timer
def strip_parallelized(folder, cores=1):
    return Parallel(n_jobs=cores)(delayed(strip_folder)(os.path.join(folder, year)) for year in sorted(os.listdir(folder)))


if __name__ == '__main__':
    results, t = strip_parallelized('OpenSubtitles2018/raw/en', cores=92)
    print('stripped xml from {} files in {} seconds'.format(np.sum(results), int(t['duration'])))
