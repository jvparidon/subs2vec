# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import argparse
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


def deduplicate_words(analogies_fname):
    words = set()
    with open(analogies_fname, 'r', encoding='utf-8') as analogies_file:
        [words.update(line[1].replace('\n', '').split(' ')) for line in enumerate(analogies_file) if ':' not in line[1]]
    words = sorted(list(words))
    words_fname = analogies_fname.replace('.txt', '.unique_words.txt')
    with open(words_fname, 'w', encoding='utf-8') as words_file:
        words_file.write('\n'.join(words))
    logging.info('wrote {} unique words to {}'.format(len(words), words_fname))


def rebuild_analogies(analogies_fname, translations_fname, lang):
    with open(translations_fname, 'r', encoding='utf-8') as translations_file:
        dictionary = {line.split('\t')[0]: line.split('\t')[1].replace('\n', '') for line in translations_file}
    new_fname = analogies_fname.split('/')
    new_fname[-1] = '{}-{}'.format(lang, new_fname[-1][3:])
    new_fname = '/'.join(new_fname)
    with open(analogies_fname, 'r', encoding='utf-8') as analogies_file, open(new_fname, 'w', encoding='utf-8') as new_file:
        for line in analogies_file:
            if (':' in line) or ('#' in line):
                new_file.write(line)
            else:
                line = line.replace('\n', '').split(' ')
                newline = [dictionary[word] for word in line]
                new_file.write('{}\n'.format(' '.join(newline)))
    logging.info('wrote translated analogies sets to {}'.format(new_fname))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='deduplicate words in analogies set for faster translation'
                                                    + '\nand then recompile the translations into an analogies set')
    argparser.add_argument('-m', '--mode', type=str, choices=['deduplicate', 'rebuild'])
    argparser.add_argument('-fa', '--analogies_filename')
    argparser.add_argument('-ft', '--translations_filename')
    argparser.add_argument('-l', '--lang')
    args = argparser.parse_args()

    if args.mode == 'deduplicate':
        deduplicate_words(args.analogies_filename)
    elif args.mode == 'rebuild':
        rebuild_analogies(args.analogies_filename, args.translations_filename, args.lang)
