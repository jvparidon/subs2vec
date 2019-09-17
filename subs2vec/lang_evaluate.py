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

    # kludge to quickly evaluate all vectors/datasets for Van Paridon & Thompson (2019)
    lang = args.lang
    filepaths = [f'../../pretrained/fasttext/cc.{lang}.300.vec',
                 f'../../for_publication/{lang}/wiki-subs.{lang}.vec',
                 f'../../for_publication/{lang}/subs.{lang}.vec',
                 f'../../for_publication/{lang}/wiki.{lang}.vec']
    for filepath in filepaths:
        if os.path.exists(filepath):
            print(filepath.split('/')[-1])
            evaluate_lang(lang=lang, vecs_fname=filepath)
