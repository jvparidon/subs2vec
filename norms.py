# coding: utf-8
# Copyright (c) 2018 - Present Bill Thompson (biltho@mpi.nl) & Jeroen van Paridon (jerpar@mpi.nl)
import numpy as np
import pandas as pd
import sklearn.linear_model
import sklearn.model_selection
import sklearn.preprocessing
import argparse
import vecs
from utensilities import log_timer
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)


@log_timer
def predict_norms(vectors, norms):

    norms = norms.set_index('words')
    df = norms.join(vectors, how='left').dropna()

    scaler = sklearn.preprocessing.StandardScaler()
    model = sklearn.linear_model.Ridge()
    X = scaler.fit_transform(df[vectors.columns.values])

    for col in norms.columns.values:
        y = df['ratings']
        scores = sklearn.model_selection.cross_val_score(model, X, y, cv=10)
        print(col)
        print(np.mean(scores))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='perform crossvalidated penalized regression of lexical norms using word vectors as predictors')
    argparser.add_argument('vecs_fname')
    argparser.add_argument('norms_fname')
    args = argparser.parse_args()

    norms = pd.read_csv('aoa-en-kuperman-2012.csv')
    vectors = vecs.Vectors(args.vecs_fname, normalize=True, n=2e5).as_df()
    predict_norms(vectors, norms)
