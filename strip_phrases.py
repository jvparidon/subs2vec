import argparse
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


def strip_phrases(filename):
    if filename.endswith('.vec') is False:
        raise ValueError('{} does not have a .vec extension, please specify a valid .vec file'.format(filename))
    logging.info('stripping linked phrases from {}'.format(filename))
    out_fname = filename.replace('.vec', '.nophrases.vec')
    with open(filename, 'r', encoding='utf-8') as in_file, open(out_fname, 'w', encoding='utf-8') as out_file:
        lines = 0
        new_lines = 0
        for line in in_file:
            lines += 1
            if '_' not in line.split(' ')[0]:
                out_file.write(line)
                new_lines += 1
    logging.info('read {} lines, removed {} linked phrases, wrote {} word vectors to {}'
                 .format(lines, lines - new_lines, new_lines, out_fname))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='remove linked phrases of the type "peanut_butter" from a .vec file')
    argparser.add_argument('-f', '--filename', help='file to strip', required=True)
    args = argparser.parse_args()

    strip_phrases(**vars(args))
