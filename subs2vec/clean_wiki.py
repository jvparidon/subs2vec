"""Clean Wikipedia dumps for use as a training corpus."""
import re
import argparse
import html
import bz2
import logging
from .utensils import log_timer
from multiprocessing import cpu_count
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
cores = int(cpu_count() / 2)


@log_timer
def strip_wiki_file(fname):
    """Strip xml and other tags from Wikipedia dump.

    Writes stripped Wikipedia text directly to text file.

    :param fname: Wikipedia dump file, in xml or bzip2 format.
    """
    logging.info(f'stripping {fname}')
    if fname.endswith('.bz2'):
        with bz2.open(fname, 'rt', encoding='utf-8') as in_file, open(fname.replace('.xml.bz2', '.txt'), 'w', encoding='utf-8') as out_file:
            out_file.write(_strip_wiki_xml(in_file.read()))
    if fname.endswith('.xml'):
        with open(fname, 'r', encoding='utf-8') as in_file, open(fname.replace('.xml', '.txt'), 'w', encoding='utf-8') as out_file:
            out_file.write(_strip_wiki_xml(in_file.read()))
    logging.info(f'completed stripping {fname}')


@log_timer
def big_strip_wiki_file(fname, lines_per_chunk=1e6):
    """Strip xml and other tags from a Wikipedia dump that doesn't fit into RAM.

    Processes Wikipedia dump in chunks and then concatenates the junks into a single text file.

    :param fname: Wikipedia dump file, in xml or bzip2 format.
    :param lines_per_chunk: number of lines in each chunk (default is 1e6, one million lines)
    """
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
                        out_file.write(_strip_wiki_xml(''.join(lines)))
                        lines = []
                        j += 1
                        print(j)
                else:
                    if text:
                        lines.append(line)
                        i += 1
            out_file.write(_strip_wiki_xml(''.join(lines)))

    if fname.endswith('.xml'):
        with open(fname, 'r', encoding='utf-8') as in_file, open(fname.replace('.xml', '.txt'), 'w', encoding='utf-8') as out_file:
            out_file.write(_strip_wiki_xml(in_file.read()))
    logging.info(f'completed stripping {fname}')


def _strip_curly(txt):
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


regeces = [
    (r'(?s)<ref.*?</ref>', ''),  # strip reference links
    (r'(?s)<references.*?</references>', ''),  # strip references
    (r'(?s)<table.*?</table>', ''),  # strip tables
    (r'(?s)<gallery.*?</gallery>', ''),  # strip galleries
    (r'(?s)<kml.*?</kml>', ''),  # strip KML tags
    (r'<.*?>', ''),  # strip other xml tags
    (r'http.*?(?:[\s\n\]]|$)', ''),  # strip external http(s) links
    (r'\[\[[^\]]*?:.*\|(.*?)\]\]', '\\1'),  # strip links to files, etc. but keep labels
    (r'\[\[[^\]]*?:(.*?)\]\]', ''),  # strip category links
    (r'\[\[[^\]]*?\|(.*?)\]\]', '\\1'),  # convert labeled links to just labels
    (r'(?m)^[\s]*[!?*;:=+\-|#_].*?$', ''),  # strip lines that do not start with alphanumerics, quotes, or brackets
    (r'(?m)^.*?\(UTC\).*?$', ''),  # strip lines containing a time stamp
    (r'\s\(.*?\)', ''),  # remove everything in parentheses
    (r'([^\s.!?:;]{2})[.!?:;]+?[\s\n]|$', '\\1\n'),  # break sentences at periods
    (r"[-–—/']", ' '),  # replace hyphens, apostrophes and slashes with spaces
    (r'\s*\n\s*', '\n'),  # strip empty lines and lines containing whitespace
    (r'\s{2,}', ' '),  # strip excessive spaces
]
patterns = [(re.compile(regec[0], re.IGNORECASE), regec[1]) for regec in regeces]
def _strip_wiki_xml(txts):
    """Strip xml and other tags from Wikipedia text.

    :param txts: Wikipedia dump text containing multiple articles
    :return: stripped Wikipedia text
    """
    pattern = re.compile('<text.*?>(.*?)</text>', re.DOTALL)
    txts = pattern.findall(html.unescape(html.unescape(txts)))  # double unescape because Wikipedia dumps are a mess

    txts = [_strip_curly(txt) if ((not txt.startswith('#'))
                                 and ('<noinclude>' not in txt.lower())
                                 and ('__noindex__' not in txt.lower())
                                 ) else '' for txt in txts]

    for i in range(len(txts)):
        for pattern in patterns:
            txts[i] = pattern[0].sub(pattern[1], txts[i])

    txts = [''.join([letter for letter in txt if (letter.isalnum() or letter.isspace())]) for txt in txts if txt != '']
    return '\n'.join(txts)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='strip Wikipedia dumps of xml and other tags')
    argparser.add_argument('fname', help='name of Wikipedia dump file')
    argparser.add_argument('--big', action='store_true', help='use special method for files that do not fit in RAM')
    args = argparser.parse_args()

    if args.big:
        big_strip_wiki_file(fname=args.fname)
    else:
        strip_wiki_file(fname=args.fname)
