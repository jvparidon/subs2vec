import argparse
from .frequencies import count_ngrams
from .vecs import Vectors


def lang_compile(lang):
    # subs
    corpus = f'../../data/OpenSubtitles/raw/dedup.{lang}.txt'
    unigrams, _, _ = count_ngrams(corpus, kind='words')
    total = unigrams['unigram_freqs'].sum()
    print(f'{corpus}\t{total}')
    vectors = Vectors(f'subs.{lang}.vec', n=1e6)
    vectors.write_vecs(f'subs.{lang}.1e6.vec')

    # wiki
    corpus = f'../../data/wiki/dedup.{lang}.txt'
    unigrams, _, _ = count_ngrams(corpus, kind='words')
    total = unigrams['unigram_freqs'].sum()
    print(f'{corpus}\t{total}')
    vectors = Vectors(f'wiki.{lang}.vec', n=1e6)
    vectors.write_vecs(f'wiki.{lang}.1e6.vec')

    # wiki-subs
    vectors = Vectors(f'wiki-subs.{lang}.vec', n=1e6)
    vectors.write_vecs(f'wiki-subs.{lang}.1e6.vec')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='do ancillary stuff for a language')
    argparser.add_argument('lang')
    args = argparser.parse_args()

    lang_compile(args.lang)
