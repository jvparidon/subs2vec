# coding: utf-8
# Copyright (c) 2018 - Present Bill Thompson (biltho@mpi.nl) & Jeroen van Paridon (jerpar@mpi.nl)
import numpy as np
import pandas as pd
import sklearn.linear_model
import sklearn.model_selection
import sklearn.preprocessing
import argparse
import os
import vecs
from utensilities import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


@log_timer
def evaluate_vecs(lang, vecs_fname):
    vectors = vecs.Vectors(vecs_fname, normalize=True, n=1e6).as_df()
    results = []
    for norms_fname in os.listdir('evaluation/norms'):
        if norms_fname.startswith(lang):
            results.append(predict_norms(vectors, norms_fname))
    results_fname = os.path.split(vecs_fname)[1].replace('.vec', '.tsv')
    pd.concat(results).to_csv(os.path.join('results/norms', results_fname), sep='\t')


@log_timer
def predict_norms(vectors, norms_fname):
    norms = pd.read_csv(norms_fname, sep='\t')
    norms = norms.set_index('words')
    df = norms.join(vectors, how='left').dropna()

    scaler = sklearn.preprocessing.StandardScaler()  # standardize predictors
    model = sklearn.linear_model.Ridge()  # use ridge regression models
    X = scaler.fit_transform(df[vectors.columns.values])  # word vectors are the predictors

    results = []
    for col in norms.columns.values:
        # set dependent variable and calculate 10-fold mean fit/predict scores
        y = df['ratings']
        score = np.mean(sklearn.model_selection.cross_val_score(model, X, y, cv=10))
        results.append({
            'source': norms_fname.rstrip('.tsv'),
            'norm': col,
            'r': np.sqrt(score),  # take square root of explained variance to get Pearson r
            'r-squared': score
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
