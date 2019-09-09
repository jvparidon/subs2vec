"""Predict lexical norms, either to evaluate word vectors, or to get norms for unnormed words."""
# Copyright (c) 2018 - Present Bill Thompson (biltho@mpi.nl) & Jeroen van Paridon (jerpar@mpi.nl)
import numpy as np
import pandas as pd
import sklearn.linear_model
import sklearn.model_selection
import sklearn.preprocessing
import sklearn.utils
import argparse
import os
from .vecs import Vectors
from .utensils import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
path = os.path.dirname(__file__)


@log_timer
def evaluate_norms(lang, vecs_fname):
    """Predict lexical norms to evaluate a set of word vectors in a given language.
    
    Writes scores to tab-separated text file.

    :param lang: language to evaluate word vectors in (uses two-letter ISO codes)
    :param vecs_fname: word vectors to evaluate
    """
    norms_path = os.path.join(path, 'evaluation', 'datasets', 'norms')
    results_path = os.path.join(path, 'evaluation', 'results', 'norms')
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    logging.info(f'evaluating lexical norm prediction with {vecs_fname}')
    vectors = Vectors(vecs_fname, normalize=True, n=1e6, d=300)
    scores = []
    for norms_fname in os.listdir(norms_path):
        if norms_fname.startswith(lang):
            logging.info(f'predicting norms from {norms_fname}')
            norms = pd.read_csv(os.path.join(norms_path, norms_fname), sep='\t', comment='#')
            norms = norms.set_index('word')
            score = predict_norms(vectors, norms)['scores']
            score['source'] = norms_fname
            scores.append(score)
    scores_fname = os.path.split(vecs_fname)[1].replace('.vec', '.tsv')
    if len(scores) > 0:
        pd.concat(scores).to_csv(os.path.join(results_path, scores_fname), sep='\t')


@log_timer
def predict_norms(vectors, norms):
    """Predict lexical norms and return score.

    :param vectors: Vectors object containing word vectors
    :param norms: pandas DataFrame of lexical norms
    :return: dict containing scores and predictions in separate pandas DataFrames
    """
    vectors = vectors.as_df()
    cols = norms.columns.values
    df = norms.join(vectors, how='inner')
    # compensate for missing ys somehow
    total = len(norms)
    missing = len(norms) - len(df)
    penalty = (total - missing) / total
    logging.info(f'missing vectors for {missing} out of {total} words')
    df = sklearn.utils.shuffle(df)  # shuffle is important for unbiased results on ordered datasets!

    model = sklearn.linear_model.Ridge()  # use ridge regression models
    cv = sklearn.model_selection.RepeatedKFold(n_splits=5, n_repeats=10)

    # compute crossvalidated prediction scores
    scores = []
    for col in cols:
        # set dependent variable and calculate 10-fold mean fit/predict scores
        df_subset = df.loc[:,vectors.columns.values]  # use .loc[] so copy is created and no setting with copy warning is issued
        df_subset[col] = df[col]
        df_subset = df_subset.dropna()  # drop NaNs for this specific y
        x = df_subset[vectors.columns.values]
        y = df_subset[col]
        cv_scores = sklearn.model_selection.cross_val_score(model, x, y, cv=cv)
        median_score = penalty * np.median(cv_scores)
        scores.append({
            'norm': col,
            'r': np.sqrt(median_score),  # take square root of explained variance to get Pearson r
            'r-squared': median_score
        })

    # predict (extend norms)
    x_full = df[vectors.columns.values]
    predictions = df.loc[:, cols]  # use .loc[] so copy is created and no setting with copy warning is raised by pandas
    for col in cols:
        # set dependent variable and fit, but predict for whole x (so including unobserved y)
        df_subset = df.loc[:, vectors.columns.values]  # use .loc[] so copy is created and no setting with copy warning is raised
        df_subset[col] = df[col]
        df_subset = df_subset.dropna()  # drop NaNs for this specific y
        x = df_subset[vectors.columns.values]
        y = df_subset[col]
        model.fit(x, y)
        predictions[f'{col} predicted'] = model.predict(x_full)

    return {'scores': pd.DataFrame(scores), 'predictions': predictions}


def extend_norms(vecs_fname, norms_fname):
    """Extend lexical norms to unobserved words, using word vectors.

    Writes predictions to tab-separated text file.

    :param vecs_fname: File containing word vectors to use for prediction.
    :param norms_fname: File containing norms in tab-separated columns, first column should contain words,
     first line should contain column names, unobserved cells should be left empty.
    """
    logging.info(f'extending lexical norms with {vecs_fname}')
    vectors = Vectors(vecs_fname, normalize=True, n=1e6, d=300)
    norms = pd.read_csv(norms_fname, sep='\t', comment='#')
    norms = norms.set_index('word')
    results = predict_norms(vectors, norms)
    base_fname = '.'.join(norms_fname.split('.')[:-1])
    results['scores'].to_csv(f'{base_fname}.scores.tsv', sep='\t')
    results['predictions'].to_csv(f'{base_fname}.predictions.tsv', sep='\t')


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='perform crossvalidated penalized regression of lexical norms using word vectors as predictors')
    argparser.add_argument('lang')
    argparser.add_argument('vecs_fname')
    argparser.add_argument('--extend', action='store_true')
    argparser.add_argument('--norms_fname')
    args = argparser.parse_args()

    if args.extend:
        extend_norms(args.vecs_fname, args.norms_fname)
    else:
        evaluate_norms(args.lang, args.vecs_fname)
