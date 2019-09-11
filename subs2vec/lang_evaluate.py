"""Evaluate available vectors for a given language."""
import os
import argparse
from .norms import evaluate_norms
from .analogies import evaluate_analogies
from .similarities import evaluate_similarities

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('lang')
    args = argparser.parse_args()

    lang = args.lang

    langs = os.listdir('evaluation/similarities') + os.listdir('evaluation/analogies') + os.listdir('evaluation/norms')
    langs = set([lang[0:2] for lang in langs])

    filepaths = [f'../pretrained/fasttext/cc.{lang}.300.vec',
                 f'../data/wiki-sub/{lang}/wiki-sub.{lang}.vec',
                 f'../data/OpenSubtitles/raw/{lang}/sub.{lang}.vec',
                 f'../data/wiki/{lang}/wiki.{lang}.vec']
    for filepath in filepaths:
        if os.path.exists(filepath) and (lang in langs):
            print(filepath.split('/')[-1])
            evaluate_norms(lang, filepath)
            evaluate_similarities(lang, filepath)
            evaluate_analogies(lang, filepath)
