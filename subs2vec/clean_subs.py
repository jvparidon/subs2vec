"""Clean and concatenate OpenSubtitles archives into a single training corpus."""
import os
import zipfile
import argparse
import re
from .utensils import log_timer
from lxml import etree
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


def _strip_upos(tree):
    # format [word]_[POS tag]
    stripped = []
    for node in tree.iter():
        if node.tag == 's':
            stripped.append('\n')
        if node.tag == 'w':
            stripped.append(f'{node.text}_{node.get("upos")} ')
    return u''.join(stripped)


def _strip_lemma(tree):
    # format [lemmatized word]
    stripped = []
    for node in tree.iter():
        if node.tag == 's':
            stripped.append('\n')
        if node.tag == 'w':
            stripped.append(f'{node.get("lemma")}_{node.get("upos")} ')
    return u''.join(stripped)


def _strip_txt(tree):
    # format [sentence]
    for node in tree.iter():
        if node.tag == 'meta':
            tree.remove(node)
    return etree.tostring(tree, encoding=str, method='text')


def _strip_viz(tree):
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


def _strip_xml(text, xmlparser, ioformat='txt'):
    tree = etree.fromstring(text, xmlparser)
    if ioformat == 'upos':
        return _strip_upos(tree)
    elif ioformat == 'lemma':
        return _strip_lemma(tree)
    elif ioformat == 'txt':
        return _strip_txt(tree)
    elif ioformat == 'viz':
        return _strip_viz(tree)


@log_timer
def strip_archive(lang, ioformat='txt', years=(1900, 2100)):
    """Strip xml from a compressed OpenSubtitles archive.

    Writes stripped output directly to a new compressed archive.

    :param lang: language of the archive to strip (selects the correct archive)
    :param ioformat: input/output format, default is txt
    :param years: tuple of first and last year to select only subtitles from a range of years, default is 1900 to 2100
    """
    read_zip = zipfile.ZipFile(f'{lang}.zip', 'r')
    write_zip = zipfile.ZipFile(f'{lang}_stripped.zip', 'a')
    if ioformat == 'txt':
        dirpath = 'OpenSubtitles/raw'
    elif ioformat in ['upos', 'lemma']:
        dirpath = 'OpenSubtitles/parsed'
    filepaths = []
    for filepath in read_zip.namelist():
        if filepath.endswith('xml'):
            if filepath.startswith(os.path.join(dirpath, lang)):
                if int(filepath.split('/')[3]) in range(*years):
                    filepaths.append(filepath)
    logging.info(f'stripping xml from {len(filepaths)} subtitles in {lang}')
    # XML parser recover option is needed to deal with malformed XML in subs
    xmlparser = etree.XMLParser(recover=True, encoding='utf-8')
    for filepath in sorted(filepaths):
        write_zip.writestr(filepath.replace('xml', ioformat),
                           _strip_xml(read_zip.open(filepath).read(), xmlparser, ioformat))


regeces = [
    (r'<.*?>', ''),  # strip other xml tags
    (r'http.*?(?:[\s\n\]]|$)', ''),  # strip links
    (r'\s\(.*?\)', ''),  # remove everything in parentheses
    (r'([^\s]{2,})[\.\!\?\:\;]+?[\s\n]|$', '\\1\n'),  # break sentences at periods
    (r"[-–—/']", ' '),  # replace hyphens, apostrophes and slashes with spaces
    (r'\s*\n\s*', '\n'),  # strip empty lines and lines containing whitespace
    (r'\s{2,}', ' '),  # strip excessive spaces
]
patterns = [(re.compile(regec[0], re.IGNORECASE), regec[1]) for regec in regeces]
def _strip_punctuation(txt, ioformat='txt'):
    """Strip punctuation from a string of text.

    :param txt: text to strip punctuation from
    :param ioformat: input/output format, default is txt
    :return: stripped text
    """

    for pattern in patterns:
        txt = pattern[0].sub(pattern[1], txt)
    if ioformat == 'txt':
        txt = ''.join([letter for letter in txt if (letter.isalnum() or letter.isspace())])
    elif ioformat in ['lemma', 'upos']:
        txt = ''.join([letter for letter in txt if (letter.isalnum() or letter.isspace() or (letter == '_'))])
    else:
        txt = ''.join([letter for letter in txt if (letter.isalnum() or letter.isspace())])
    return txt


@log_timer
def join_archive(lang, ioformat='txt', years=(1900, 2050), verbose=False):
    """Concatenate a stripped OpenSubtitles archive into a single training corpus.

    :param lang: language of the archive to join (selects the correct archive)
    :param ioformat: input/output format (default is txt)
    :param years: tuple of first and last year to select only subtitles from a range of years, default is 1900 to 2100.
    :param verbose: boolean setting whether or not to print a progress bar to the command line, default is False
    :return: number of files that were concatenated
    """
    read_zip = zipfile.ZipFile(f'{lang}_stripped.zip', 'r')
    out_fname = f'{lang}.{ioformat}'
    if ioformat == 'txt':
        dirpath = 'OpenSubtitles/raw'
    elif ioformat in ['upos', 'lemma']:
        dirpath = 'OpenSubtitles/parsed'
    filepaths = []
    for filepath in read_zip.namelist():
        if filepath.endswith(ioformat):
            if filepath.startswith(os.path.join(dirpath, lang)):
                if int(filepath.split('/')[3]) in range(*years):
                    filepaths.append(filepath)
    total = len(filepaths)
    logging.info(f'joining {len(filepaths)} subtitles in {lang} into a single file')
    i = 0
    with open(out_fname, 'w') as outfile:
        for filepath in filepaths:
                outfile.write(_strip_punctuation(read_zip.open(filepath).read().decode('utf-8'), ioformat))
                if verbose:
                    i += 1
                    print(f'\tprogress: {(float(i) / total) * 100:5.2f}%', end='\r')
        if verbose:
            print('')
    return total


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='clean subtitles for training distributional semantics models')
    argparser.add_argument('lang', help='language to clean')
    argparser.add_argument('--strip', action='store_true', help='strip xml from subtitles archive')
    argparser.add_argument('--years', default=(1900, 2050), nargs=2, type=int, help='range of years to include')
    argparser.add_argument('--join', action='store_true', help='concatenate stripped archive')
    argparser.add_argument('--ioformat', default='txt', choices=['txt', 'lemma', 'upos', 'viz'],
                           help='input/output format')
    args = argparser.parse_args()

    if args.strip:
        strip_archive(lang=args.lang, ioformat=args.ioformat, years=args.years)
    if args.join:
        join_archive(lang=args.lang, ioformat=args.ioformat, years=args.years)
