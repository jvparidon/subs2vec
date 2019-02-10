import re
import argparse
import html
import bz2
import os
import logging
from joblib import Parallel, delayed
from multiprocessing import cpu_count
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
cores = int(cpu_count() / 2)


def strip_wiki_file(fname):
    logging.info(f'stripping {fname}')
    if fname.endswith('.bz2'):
        with bz2.open(fname, 'rt', encoding='utf-8') as in_file, open(fname.replace('.xml.bz2', '.txt'), 'w', encoding='utf-8') as out_file:
            out_file.write(strip_wiki_xml(in_file.read()))
    if fname.endswith('.xml'):
        with open(fname, 'r', encoding='utf-8') as in_file, open(fname.replace('.xml', '.txt'), 'w', encoding='utf-8') as out_file:
            out_file.write(strip_wiki_xml(in_file.read()))
    logging.info(f'completed stripping {fname}')


def strip_curly(txt):
    curly = 0
    txt = list(txt)
    for i in range(len(txt)):
        if txt[i] == '{':
            curly += 1
        elif txt[i] == '}':
            curly -= 1
            txt[i] = ''
        if curly > 0:
            txt[i] = ''
        elif curly < 0:
            # there appear to be more closing than opening brackets in this lemma, we should just discard it
            txt = []
            break
    return ''.join(txt)


def strip_wiki_xml(txts):
    pattern = re.compile('<text.*?>(.*?)</text>', re.DOTALL)
    txts = pattern.findall(html.unescape(html.unescape(txts)))

    regeces = [
        ('(?s)<ref.*?</ref>', ''),  # strip reference links
        ('(?s)<references.*?</references>', ''),  # strip references
        ('(?s)<table.*?</table>', ''),  # strip tables
        ('(?s)<gallery.*?</gallery>', ''),  # strip galleries
        ('(?s)<kml.*?</kml>', ''),  # strip KML tags
        ('<.*?>', ''),  # strip other xml tags
        ('http.*?(?:[\s\n\]]|$)', ''),  # strip links
        ('(?s)\[{2}[^\]]*?:.*?\]{2}', ''),  # strip all special links (categories, files, etc.)
        ('\[\[.*?\|(.*?)\]\]', '\\1'),  # convert labeled links to just labels
        ('(?m)^[*=+\-].*?$', ''),  # strip lines that do not start with a-z or [
        ('([^\s]{2})[\.\?\!]', '\\1\n'),  # line breaks at sentence ends, but not single initials
        ('\n+', '\n'),  # strip excessive line endings
        ('(?:^\n|\n$)', ''),  # strip line endings at either end of strings
        ('[-–]', '-'),  # replace different types of dash with hyphen
        ('[—/]', ' '),  # replace ellipses and slashes with spaces
    ]
    txts = [strip_curly(txt) if (('#redirect' not in txt.lower())
                                 and ('<noinclude>' not in txt)
                                 and ('__noindex__' not in txt.lower())
                                 ) else '' for txt in txts]
    for regec in regeces:
        pattern = re.compile(regec[0], re.IGNORECASE)
        for i in range(len(txts)):
            txts[i] = pattern.sub(regec[1], txts[i])
    txts = [''.join([letter for letter in txt if (letter.isalnum() or letter.isspace() or (letter == '-'))]) for txt in txts if txt != '']
    return '\n'.join(txts)


def strip_parallelized(folder, cores=1):
    return Parallel(n_jobs=cores)(delayed(strip_wiki_file)(os.path.join(folder, fname)) for fname in sorted(os.listdir(folder)))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='strip wikipedia dumps of xml and other tags')
    argparser.add_argument('--filename', help='')
    argparser.add_argument('--directory', help='overrides filename')
    args = argparser.parse_args()

    if args.directory:
        strip_parallelized(args.directory)
    elif args.filename:
        strip_wiki_file(args.filename)
