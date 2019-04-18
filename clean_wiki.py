import re
import argparse
import html
import bz2
import os
import logging
from utensilities import log_timer
from joblib import Parallel, delayed
from multiprocessing import cpu_count
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
cores = int(cpu_count() / 2)


@log_timer
def strip_wiki_file(fname):
    logging.info(f'stripping {fname}')
    if fname.endswith('.bz2'):
        with bz2.open(fname, 'rt', encoding='utf-8') as in_file, open(fname.replace('.xml.bz2', '.txt'), 'w', encoding='utf-8') as out_file:
            out_file.write(strip_wiki_xml(in_file.read()))
    if fname.endswith('.xml'):
        with open(fname, 'r', encoding='utf-8') as in_file, open(fname.replace('.xml', '.txt'), 'w', encoding='utf-8') as out_file:
            out_file.write(strip_wiki_xml(in_file.read()))
    logging.info(f'completed stripping {fname}')


# TODO: figure out if 1e7 is a sensible number of lines for this (equates to approx. 500MB temp files)
@log_timer
def big_strip_wiki_file(fname, lines_per_chunk=1e7):
    logging.info(f'stripping {fname}')
    if fname.endswith('.bz2'):
        with bz2.open(fname, 'rt', encoding='utf-8') as in_file, open(fname.replace('.xml.bz2', '.txt'), 'w', encoding='utf-8') as out_file:

            i = 0
            j = 0
            temp_file = open(f'temp{j}.txt', 'w')
            for line in in_file:
                if i > ((j + 1) * int(lines_per_chunk)):
                    if '<text' in line:
                        temp_file.close()
                        j += 1
                        temp_file = open(f'temp{j}.txt', 'w')
                temp_file.write(line)
                i += 1
            temp_file.close()

            for k in range(j + 1):
                with open(f'temp{k}.txt', 'r') as temp_file:
                    out_file.write(strip_wiki_xml(temp_file.read()))

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
        (r'([^\s]{2})[\.\?\!]+', '\\1\n'),  # line breaks at sentence ends, but not single initials
        (r'[-–]', '-'),  # replace different types of dash with hyphen
        (r'[—/]', ' '),  # replace ellipses and slashes with spaces
        (r'-\s', ' '),  # strip hyphens outside of compounds
        (r' {2,}', ' '),  # strip excessive spaces
        (r'\s*\n\s*', '\n'),  # strip empty lines
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
    argparser.add_argument('--filename')
    argparser.add_argument('--directory', help='overrides filename')
    argparser.add_argument('--big', action='store_true', help='for files that do not fit in memory')
    args = argparser.parse_args()

    if args.directory:
        strip_parallelized(args.directory)
    elif args.filename:
        if args.big:
            big_strip_wiki_file(args.filename)
        else:
            strip_wiki_file(args.filename)
