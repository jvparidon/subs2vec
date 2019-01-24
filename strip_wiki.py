import re
import argparse
import html


def strip_wiki_file(fname):
    with open(fname, 'r', encoding='utf-8') as in_file, open(fname.replace('.xml', '.linebreaks.txt'), 'w', encoding='utf-8') as out_file:
        out_file.write(strip_wiki_xml(in_file.read()))


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


def strip_wiki_xml(txt):
    # pattern = re.compile('<div.*?>.*?</div>', re.DOTALL)
    # txt = pattern.sub('', txt)
    pattern = re.compile('<text.*?>(.*?)</text>', re.DOTALL)
    txts = pattern.findall(html.unescape(txt))

    regeces = [
        ('<ref.*?</ref>', ''),
        ('<.*?>', ''),
        ('<[^>]*?>', ''),
        #('http.*?[\s|\]]', ''),
        #('\|thumb', ''),
        #('\|left', ''),
        #('\|right', ''),
        #('\|\d+px', ''),
        ('\[\[image:[^\[\]]*\|.*', ''),
        ('\[\[file:[^\[\]]*\|.*', ''),
        ('\[\[category:([^|\]]*)[^]]*\]\]', '[[\\1]]'),
        ('\n(\[\[.*?\]\]\n)+', '\n'),
        ('\[\[.*?\|(.*?)\]\]', '\\1'),
        ('\[\[(.*?)\]\]', '\\1'),
        #('\[\[[a-z\-]*:[^\]]*\]\]', ''),
        #('\[\[[^\|\]]*\|', '[['),
        #('\{\{[^\}]*\}\}', ''),
        #('\{[^\}]*\}', ''),
        #('\n\s*\|.*', ''),
        #('\n\s*\!.*', ''),
        #('\n\s*:.*', ''),
        ('\n\s*file:.*', ''),
        ('\n\s*\*.*', ''),
        ('\s*==.*?\n', ''),
        ('\.', '\n'),
        ('\n\n*', '\n')
    ]
    txts = [strip_curly(txt) if (('#redirect' not in txt.lower())
                                 and ('<noinclude>' not in txt)
                                 and ('__noindex__' not in txt.lower())
                                 # and ('{{cite' not in txt)
                                 # and ('{{user' not in txt)
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
