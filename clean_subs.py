import os
import zipfile
import argparse
from utensilities import log_timer
from lxml import etree
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


def strip_upos(tree):
    # format [word]_[POS tag]
    stripped = []
    for node in tree.iter():
        if node.tag == 's':
            stripped.append('\n')
        if node.tag == 'w':
            stripped.append(f'{node.text}_{node.get("upos")} ')
    return u''.join(stripped)


def strip_lemma(tree):
    # format [lemmatized word]
    stripped = []
    for node in tree.iter():
        if node.tag == 's':
            stripped.append('\n')
        if node.tag == 'w':
            stripped.append(f'{node.get("lemma")} ')
    return u''.join(stripped)


def strip_txt(tree):
    # format [sentence]
    for node in tree.iter():
        if node.tag == 'meta':
            tree.remove(node)
    return etree.tostring(tree, encoding=str, method='text')


def strip_viz(tree):
    # format [timestamp in ms] [sentence]
    stripped = []
    for node in tree.iter():
        if node.tag == 's':
            children = list(node)
            if len(children) > 0:
                if children[0].tag == 'time':
                    timestamp = children[0].get('value').replace(':', '').replace(',', '.')
                    txt = etree.tostring(node, encoding=str, method='text').replace('\n', '')
                    stripped.append(f'[{timestamp}] {txt}')
    return u'\n'.join(stripped)


def strip_xml(text, xmlparser, ioformat='txt'):
    tree = etree.fromstring(text, xmlparser)
    if ioformat == 'upos':
        return strip_upos(tree)
    elif ioformat == 'lemma':
        return strip_lemma(tree)
    elif ioformat == 'txt':
        return strip_txt(tree)
    elif ioformat == 'viz':
        return strip_viz(tree)


@log_timer
def strip_archive(lang, ioformat='txt', years=(1900, 2050)):
    read_zip = zipfile.ZipFile(f'{lang}.zip', 'r')
    write_zip = zipfile.ZipFile(f'{lang}_stripped.zip', 'a')
    dirpath = 'OpenSubtitles/raw'
    filepaths = []
    for filepath in read_zip.namelist():
        if filepath.endswith('xml'):
            if filepath.startswith(os.path.join(dirpath, lang)):
                if int(filepath.split('/')[3]) in range(*years):
                    filepaths.append(filepath)
    logging.info(f'stripping xml from {len(filepaths)} subtitles in {lang}')
    # XML parser recover option is needed to deal with malformed XML in subs
    xmlparser = etree.XMLParser(recover=True, encoding='utf-8')
    for filename in filepaths:
        write_zip.writestr(filename.replace('xml', ioformat),
                           strip_xml(read_zip.open(filename).read(), xmlparser, ioformat))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='clean subtitles for training distributional semantics models')
    argparser.add_argument('lang', help='language to clean')
    argparser.add_argument('--ioformat', default='txt', choices=['txt', 'lemma', 'upos', 'viz'],
                           help='input/output format')
    args = argparser.parse_args()

    strip_archive(args.lang, args.ioformat)
