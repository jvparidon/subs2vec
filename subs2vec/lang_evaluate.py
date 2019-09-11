"""Evaluate a set of vectors for a given language."""
import os
import argparse
from .norms import evaluate_norms
from .analogies import evaluate_analogies
from .similarities import evaluate_similarities
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


def evaluate_lang(lang, vecs_fname):
    """Evaluate a set of vectors on all available metrics.

    :param lang: language to evaluate
    :param vecs_fname: .vec file containing word vectors
    """
    logging.info(f'evaluating {vecs_fname} with all evaluation datasets available in {lang}')
    evaluate_norms(lang, vecs_fname)
    evaluate_similarities(lang, vecs_fname)
    evaluate_analogies(lang, vecs_fname)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('lang')
    args = argparser.parse_args()

    lang = args.lang

    # kludge to quickly evaluate all vectors/datasets for Van Paridon & Thompson (2019)
    langs = os.listdir('evaluation/similarities') + os.listdir('evaluation/analogies') + os.listdir('evaluation/norms')
    langs = set([lang[0:2] for lang in langs])
    filepaths = [f'../pretrained/fasttext/cc.{lang}.300.vec',
                 f'../data/wiki-sub/{lang}/wiki-sub.{lang}.vec',
                 f'../data/OpenSubtitles/raw/{lang}/sub.{lang}.vec',
                 f'../data/wiki/{lang}/wiki.{lang}.vec']
    for filepath in filepaths:
        if os.path.exists(filepath) and (lang in langs):
            print(filepath.split('/')[-1])
            evaluate_lang(lang=lang, vecs_fname=filepath)
