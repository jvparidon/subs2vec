# coding: utf-8
# Copyright (c) 2018 - Present Bill Thompson (biltho@mpi.nl) & Jeroen van Paridon (jerpar@mpi.nl)
import numpy as np
import pandas as pd
import sklearn.linear_model
import sklearn.model_selection
import sklearn.preprocessing
import sklearn.utils
import argparse
import os
import vecs
from utensils import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
path = os.path.dirname(__file__)


@log_timer
def evaluate_vecs(lang, vecs_fname):
    norms_path = os.path.join(path, 'evaluation', 'datasets', 'norms')
    logging.info(f'evaluating lexical norm prediction with {vecs_fname}')
    vectors = vecs.Vectors(vecs_fname, normalize=True, n=1e6, d=300).as_df()
    results = []
    for norms_fname in os.listdir(norms_path):
        if norms_fname.startswith(lang):
            results.append(predict_norms(vectors, os.path.join(norms_path, norms_fname)))
    results_fname = os.path.split(vecs_fname)[1].replace('.vec', '.tsv')
    if len(results) > 0:
        pd.concat(results).to_csv(os.path.join(path, 'evaluation', 'results', 'norms', results_fname), sep='\t')


@log_timer
def predict_norms(vectors, norms_fname):
    logging.info(f'predicting norms from {norms_fname}')
    norms = pd.read_csv(norms_fname, sep='\t', comment='#')
    norms = norms.set_index('word')
    df = norms.join(vectors, how='left')
    logging.info(f'missing vectors for {df[0].isna().sum()} out of {df[0].size} words')
    df = sklearn.utils.shuffle(df.dropna())  # shuffle is important for ordered datasets!

    scaler = sklearn.preprocessing.StandardScaler()  # standardize predictors
    model = sklearn.linear_model.Ridge()  # use ridge regression models
    X = df[vectors.columns.values]
    cv = sklearn.model_selection.RepeatedKFold(n_splits=5, n_repeats=10)

    results = []
    for col in norms.columns.values:
        # set dependent variable and calculate 10-fold mean fit/predict scores
        y = df[col]
        scores = sklearn.model_selection.cross_val_score(model, X, y, cv=cv)
        median_score = np.median(scores)
        results.append({
            'source': norms_fname.rstrip('.tsv'),
            'norm': col,
            'r': np.sqrt(median_score),  # take square root of explained variance to get Pearson r
            'r-squared': median_score
        })

    return pd.DataFrame(results)


@log_timer
def extend_norms(vecs_fname, norms_fname):
    # implement extension of lexical norms using pandas and ridge regression fit/predict
    pass


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='perform crossvalidated penalized regression of lexical norms using word vectors as predictors')
    argparser.add_argument('lang')
    argparser.add_argument('vecs_fname')
    args = argparser.parse_args()

    evaluate_vecs(args.lang, args.vecs_fname)
