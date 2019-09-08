import re
import argparse
import html
import bz2
import os
import logging
from .utensils import log_timer
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
def big_strip_wiki_file(fname, lines_per_chunk=1e6):
    logging.info(f'stripping {fname}')
    if fname.endswith('.bz2'):
        with bz2.open(fname, 'rt', encoding='utf-8') as in_file, open(fname.replace('.xml.bz2', '.txt'), 'w', encoding='utf-8') as out_file:

            i = 0
            j = 0
            lines = []
            text = False
            for line in in_file:
                if '<text' in line:
                    lines.append(line)
                    text = True
                elif '</text' in line:
                    lines.append(line)
                    text = False
                    if i > ((j + 1) * int(lines_per_chunk)):
                        out_file.write(strip_wiki_xml(''.join(lines)))
                        lines = []
                        j += 1
                        print(j)
                else:
                    if text:
                        lines.append(line)
                        i += 1
            out_file.write(strip_wiki_xml(''.join(lines)))

            '''
            i = 0
            j = 0
            temp_file = open(f'{fname}_temp_{j}.txt', 'w')
            for line in in_file:
                if i > ((j + 1) * int(lines_per_chunk)):
                    if '<text' in line:
                        temp_file.close()
                        j += 1
                        temp_file = open(f'{fname}_temp_{j}.txt', 'w')
                temp_file.write(line)
                i += 1
            temp_file.close()

            for k in range(j + 1):
                with open(f'{fname}_temp_{k}.txt', 'r') as temp_file:
                    out_file.write(strip_wiki_xml(temp_file.read()))
            '''

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
    txts = pattern.findall(html.unescape(html.unescape(txts)))  # double unescape because Wikipedia is a mess

    regeces = [
        (r'(?s)<ref.*?</ref>', ''),  # strip reference links
        (r'(?s)<references.*?</references>', ''),  # strip references
        (r'(?s)<table.*?</table>', ''),  # strip tables
        (r'(?s)<gallery.*?</gallery>', ''),  # strip galleries
        (r'(?s)<kml.*?</kml>', ''),  # strip KML tags
        (r'<.*?>', ''),  # strip other xml tags
        (r'http.*?(?:[\s\n\]]|$)', ''),  # strip external http(s) links
        #(r'(?s)\[{2}[^\]]*?:.*?\]{2}', ''),  # strip all special links (categories, files, etc.)
        (r'\[\[[^\]]*?:.*\|(.*?)\]\]', '\\1'),  # strip links to files, etc. but keep labels
        (r'\[\[[^\]]*?:(.*?)\]\]', ''),  # strip category links
        (r'\[\[[^\]]*?\|(.*?)\]\]', '\\1'),  # convert labeled links to just labels
        (r'(?m)^[\s]*[!?*;:=+\-|#_].*?$', ''),  # strip lines that do not start with alphanumerics, quotes, or brackets
        (r'(?m)^.*?\(UTC\).*?$', ''),  # strip lines containing a time stamp
        #(r'[\[\]]', ''),  # remove brackets
        #(r'"+', '"'),  # remove multiple double quotes
        #(r"'+", "'"),  # remove multiple single quotes
        (r'\s\(.*?\)', ''),  # remove everything in parentheses
        (r'([^\s.!?:;]{2})[.!?:;]+?[\s\n]|$', '\\1\n'),  # break sentences at periods
        (r"[-–—/']", ' '),  # replace hyphens, apostrophes and slashes with spaces
        (r'\s*\n\s*', '\n'),  # strip empty lines and lines containing whitespace
        (r'\s{2,}', ' '),  # strip excessive spaces
    ]

    txts = [strip_curly(txt) if ((not txt.startswith('#'))
                                 and ('<noinclude>' not in txt.lower())
                                 and ('__noindex__' not in txt.lower())
                                 ) else '' for txt in txts]
    for regec in regeces:
        pattern = re.compile(regec[0], re.IGNORECASE)
        #print(regec[0])
        for i in range(len(txts)):
            #print(regec[0])
            #print(len(txts[i]))
            #print(txts[i][:20])
            #print(txts[i][-20:])
            txts[i] = pattern.sub(regec[1], txts[i])
    txts = [''.join([letter for letter in txt if (letter.isalnum() or letter.isspace())]) for txt in txts if txt != '']
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
