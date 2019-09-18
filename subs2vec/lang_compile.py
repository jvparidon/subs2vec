import argparse
from .frequencies import count_ngrams
from .vecs import Vectors


def render_wordcount(wordcount):
    if wordcount > 10000000000:
        prettycount = '{: >6}B'.format(int(wordcount / 1000000000))
    elif wordcount > 10000000:
        prettycount = '{: >6}M'.format(int(wordcount / 1000000))
    elif wordcount > 10000:
        prettycount = '{: >6}K'.format(int(wordcount / 1000))
    else:
        prettycount = '{: >6}'.format(wordcount)
    return prettycount


def lang_compile(lang):
    # subs
    corpus = f'../../data/OpenSubtitles/raw/{lang}/dedup.{lang}.txt'
    unigrams, _, _ = count_ngrams(corpus, kind='words')
    total = unigrams['unigram_freq'].sum()
    print(f'| | {lang} | OpenSubtitles | subs.{lang}.1M.vec | {render_wordcount(total)} | dedup.{lang}.words.unigrams.tsv dedup.{lang}.words.bigrams.tsv dedup.{lang}.words.trigrams.tsv |')
    vectors = Vectors(f'subs.{lang}.vec', n=1e6)
    vectors.write_vecs(f'subs.{lang}.1e6.vec')

    # wiki
    corpus = f'../../data/wiki/{lang}/dedup.{lang}wiki-meta.txt'
    unigrams, _, _ = count_ngrams(corpus, kind='words')
    total = unigrams['unigram_freq'].sum()
    print(f'| | | Wikipedia | wiki.{lang}.1M.vec | {render_wordcount(total)} | |')
    vectors = Vectors(f'wiki.{lang}.vec', n=1e6)
    vectors.write_vecs(f'wiki.{lang}.1e6.vec')

    # wiki-subs
    vectors = Vectors(f'wiki-subs.{lang}.vec', n=1e6)
    vectors.write_vecs(f'wiki-subs.{lang}.1e6.vec')
    print(f'| | | Wikipedia + OpenSubtitles | wiki-subs.{lang}.1M.vec | | |')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='do ancillary stuff for a language')
    argparser.add_argument('lang')
    args = argparser.parse_args()

    lang_compile(args.lang)
