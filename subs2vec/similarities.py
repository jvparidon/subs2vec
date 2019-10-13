"""Compute rank correlations between word vector cosine similarities and human ratings of semantic similarity."""
import numpy as np
import pandas as pd
import argparse
import os
import scipy.spatial.distance
import scipy.stats
from .vecs import Vectors
from .utensils import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
path = os.path.dirname(__file__)


@log_timer
def compare_similarities(vectors, similarities):
    """Correlate vector similarities to human ratings of semantic similarity.

    Computes cosine similarities, and uses rank (Spearman) correlation as a measure of similarity to the specified human ratings.

    :param vectors: Vectors object containing word vectors.
    :param similarities: pandas DataFrame of similarities, labeled word1, word2, and similarity
    :return: dict containing score and predictions in separate pandas DataFrames
    """
    vecs_dict = vectors.as_dict()
    vecs_dsm = []
    similarities_dsm = []
    word1 = []
    word2 = []
    missing = 0

    for index, pair in similarities.iterrows():
        if all(word in vecs_dict.keys() for word in (pair['word1'], pair['word2'])):
            vecs_dsm.append(1.0 - scipy.spatial.distance.cosine(vecs_dict[pair['word1']], vecs_dict[pair['word2']]))
            similarities_dsm.append(pair['similarity'])
            word1.append(pair['word1'])
            word2.append(pair['word2'])
        else:
            missing += 1

    total = len(similarities)
    penalty = (total - missing) / total
    score = scipy.stats.spearmanr(similarities_dsm, vecs_dsm)[0]
    adjusted_score = scipy.stats.spearmanr(similarities_dsm, vecs_dsm)[0] * penalty
    score = pd.DataFrame({'rank r': [score], 'adjusted rank r': [adjusted_score]})
    predictions = pd.DataFrame({'word1': word1, 'word2': word2, 'similarity': similarities_dsm, 'predicted similarity': vecs_dsm})
    return {'scores': score, 'predictions': predictions}


@log_timer
def evaluate_similarities(lang, vecs_fname):
    """Compute similarities for all available ratings datasets for a set of word vectors in a given language.

    Writes scores to tab-separated text file but also returns them.

    :param lang: language to evaluate word vectors in (uses two-letter ISO codes)
    :param vecs_fname: word vectors to evaluate
    :return: pandas DataFrame containing the similarities results
    """
    similarities_path = os.path.join(path, 'datasets', 'similarities')
    if not os.path.exists('results'):
        os.mkdir('results')
    results_path = os.path.join('results', 'similarities')
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    logging.info(f'evaluating semantic similarities with {vecs_fname}')
    vectors = Vectors(vecs_fname, normalize=True, n=1e6, d=300)
    scores = []
    for similarities_fname in os.listdir(similarities_path):
        if similarities_fname.startswith(lang):
            logging.info(f'correlating similarities from {similarities_fname}')
            similarities = pd.read_csv(os.path.join(similarities_path, similarities_fname), sep='\t', comment='#')
            score = compare_similarities(vectors, similarities)['scores']
            score['source'] = similarities_fname
            scores.append(score)
    scores_fname = os.path.split(vecs_fname)[1].replace('.vec', '.tsv')
    if len(scores) > 0:
        scores = pd.concat(scores)
        scores.to_csv(os.path.join(results_path, scores_fname), sep='\t')
        return scores


def novel_similarities(vecs_fname, similarities_fname):
    """Predict semantic similarities for novel word pairs, using word vectors.

    Writes predictions to tab-separated text file.

    :param vecs_fname: file containing word vectors to use for prediction.
    :param similarities_fname: file containing word pairs in tab-separated columns named 'word1' and 'word2'
    """
    logging.info(f'predicting novel semantic similarities with {vecs_fname}')
    vectors = Vectors(vecs_fname, normalize=True, n=1e6, d=300)
    vecs_dict = vectors.as_dict()
    similarities = pd.read_csv(similarities_fname, sep='\t', comment='#')
    similarities['similarity'] = similarities.apply(lambda x: 1.0 - scipy.spatial.distance.cosine(vecs_dict.get(x['word1'], np.nan),
                                                                                                  vecs_dict.get(x['word2'], np.nan)),
                                                                                                  axis=1)
    base_fname = '.'.join(similarities_fname.split('.')[:-1])
    similarities.to_csv(f'{base_fname}.predictions.tsv', sep='\t')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='compute rank correlations between word vector cosine similarities and human semantic similarity ratings')
    argparser.add_argument('lang', help='language to compare simarities in (uses two-letter ISO language codes)')
    argparser.add_argument('vecs_fname', help='word vectors to evaluate')
    argparser.add_argument('--novel_similarities', help='file containing tab-separated word pairs')
    args = argparser.parse_args()

    if args.novel_similarities:
        novel_similarities(vecs_fname=args.vecs_fname, similarities_fname=args.novel_similarities)
    else:
        print(evaluate_similarities(lang=args.lang, vecs_fname=args.vecs_fname))
