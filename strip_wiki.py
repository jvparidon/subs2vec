import re
import argparse
import html


def strip_wiki_file(fname):
    with open(fname, 'r', encoding='utf-8') as in_file, open(fname.replace('.xml', '.txt'), 'w', encoding='utf-8') as out_file:
        out_file.write(strip_wiki_xml(in_file.read()))


def strip_wiki_xml(txt):
    # pattern = re.compile('<div.*?>.*?</div>', re.DOTALL)
    # txt = pattern.sub('', txt)
    pattern = re.compile('<text.*?>(.*?)</text>', re.DOTALL)
    txts = pattern.findall(html.unescape(txt).lower())

    regeces = [
        ('<.*?>', ''),
        ('<ref[^<]*?</ref>', ''),
        ('<[^>]*?>', ''),
        ('http.*?[\s|\]]', ''),
        ('\|thumb', ''),
        ('\|left', ''),
        ('\|right', ''),
        ('\|\d+px', ''),
        ('\[\[image:[^\[\]]*\|', ''),
        ('\[\[category:([^|\]]*)[^]]*\]\]', '[[\\1]]'),
        ('\[\[[a-z\-]*:[^\]]*\]\]', ''),
        ('\[\[[^\|\]]*\|', '[['),
        ('\{\{[^\}]*\}\}', ''),
        ('\{[^\}]*\}', ''),
        ('\n\s*\|.*', ''),
        ('\n\s*\!.*', ''),
        ('\n\s*:.*', ''),
        ('\n\s*\*.*', ''),
        ('\s*==.*?\n', ''),
        ('\.', '\n'),
        ('\n\n*', '\n')
    ]
    txts = [txt if (('#redirect' not in txt)
                    and ('<noinclude>' not in txt)
                    and ('__noindex__' not in txt)
                    #and ('{{cite' not in txt)
                    and ('{{user' not in txt)
                    ) else '' for txt in txts]
    for regec in regeces:
        for i in range(len(txts)):
            pattern = re.compile(regec[0], re.IGNORECASE)
            txts[i] = pattern.sub(regec[1], txts[i])
    txts = [''.join([letter for letter in txt if (letter.isalnum() or letter.isspace() or (letter == '-'))]) for txt in txts]
    return '\n'.join(txts)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--filename', help='')
    args = argparser.parse_args()

    strip_wiki_file(args.filename)
