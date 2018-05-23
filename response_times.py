# -*- coding: utf-8 -*-
# jvparidon@gmail.com
import numpy as np
import pandas as pd
import argparse
import vecs
import sklearn.linear_model
from scipy.spatial.distance import cosine
from utensilities import timer


# semantic priming LDT data, Semantic Priming Project, Hutchison et al. (2013)
@timer
def predict_ldt(vecs_dict):
    fname = '../MKB2017/SemPriming/clean_ldt_data.txt'
    df = pd.read_csv(fname, sep='\t')
    df['cosine'] = df.apply(lambda row: cosine(vecs_dict[row['target'].lower()], vecs_dict[row['prime'].lower()]), axis=1)
    df = df.replace('#NULL!', np.nan).dropna()
    df['wordpair'] = df.apply(lambda row: '{}{}'.format(row['target'].lower(), row['prime'].lower()), axis=1)
    df['sub_sess'] = df.apply(lambda row: '{}_{}'.format(row['Subject'], row['Session']), axis=1)
    x_keys = ['target_word_length',
              'target_log_word_freq',
              'target_neighborhood_density',
              #'target_LDT_z',
              #'target_naming_RT_z',
              'prime_word_length',
              'prime_log_word_freq',
              'prime_neighborhood_density']
              #'prime_LDT_z',
              #'prime_naming_RT_z']
    df = df[x_keys + ['cosine', 'wordpair', 'target.RT', 'target.ACC', 'sub_sess']]
    df = df.replace('#NULL!', np.nan)
    df = df.dropna()
    df['target.RT'] = pd.to_numeric(df['target.RT'])
    df['target.ACC'] = pd.to_numeric(df['target.ACC'])
    # filter out target.ACC == 0
    df = df[df['target.ACC'] == 1]
    # add scipy.stats.zscore column (by subject)
    df['target.RT_z'] = (df['target.RT']
                        - df.groupby('sub_sess')['target.RT'].transform(np.mean)) \
                        / df.groupby('sub_sess')['target.RT'].transform(np.std)
    # filter out -3.0 > zscore < 3.0
    df = df[(df['target.RT_z'] > -3.0) & (df['target.RT_z'] < 3.0)]
    # recalculate zscore by subject
    df['target.RT_z'] = (df['target.RT']
                        - df.groupby('sub_sess')['target.RT'].transform(np.mean)) \
                        / df.groupby('sub_sess')['target.RT'].transform(np.std)
    df = df.groupby(['wordpair']).mean()
    x = df[x_keys]
    y = df['target.RT_z']
    lm = sklearn.linear_model.LinearRegression()
    lm.fit(x, y)
    rsquared = lm.score(x, y)
    x_vecs = df[['cosine'] + x_keys]
    lm.fit(x_vecs, y)
    rsquared_vecs = lm.score(x_vecs, y)
    return rsquared_vecs, '-', '-'


# semantic priming naming data, Semantic Priming Project, Hutchison et al. (2013)
@timer
def predict_naming(vecs_dict):
    fname = '../MKB2017/SemPriming/clean_naming_data.txt'
    df = pd.read_csv(fname, sep='\t')
    df['cosine'] = df.apply(lambda row: cosine(vecs_dict[row['target'].lower()], vecs_dict[row['prime'].lower()]), axis=1)
    df = df.replace('#NULL!', np.nan).dropna()
    df['wordpair'] = df.apply(lambda row: '{}{}'.format(row['target'].lower(), row['prime'].lower()), axis=1)
    df['sub_sess'] = df.apply(lambda row: '{}_{}'.format(row['Subject'], row['Session']), axis=1)
    x_keys = ['target_word_length',
              'target_log_word_freq',
              'target_neighborhood_density',
              #'target_LDT_z',
              #'target_naming_RT_z',
              'prime_word_length',
              'prime_log_word_freq',
              'prime_neighborhood_density']
              #'prime_LDT_z',
              #'prime_naming_RT_z']
    df = df[x_keys + ['cosine', 'wordpair', 'target.RT', 'target.ACC', 'sub_sess']]
    df = df.replace('#NULL!', np.nan)
    df = df.dropna()
    df['target.RT'] = pd.to_numeric(df['target.RT'])
    df['target.ACC'] = pd.to_numeric(df['target.ACC'])
    # filter out target.ACC == 0
    df = df[df['target.ACC'] == 1]
    # add scipy.stats.zscore column (by subject)
    df['target.RT_z'] = (df['target.RT']
                        - df.groupby('sub_sess')['target.RT'].transform(np.mean)) \
                        / df.groupby('sub_sess')['target.RT'].transform(np.std)
    # filter out -3.0 > zscore < 3.0
    df = df[(df['target.RT_z'] > -3.0) & (df['target.RT_z'] < 3.0)]
    # recalculate zscore by subject
    df['target.RT_z'] = (df['target.RT']
                        - df.groupby('sub_sess')['target.RT'].transform(np.mean)) \
                        / df.groupby('sub_sess')['target.RT'].transform(np.std)
    df = df.groupby(['wordpair']).mean()
    x = df[x_keys]
    y = df['target.RT_z']
    lm = sklearn.linear_model.LinearRegression()
    lm.fit(x, y)
    rsquared = lm.score(x, y)
    x_vecs = df[['cosine'] + x_keys]
    lm.fit(x_vecs, y)
    rsquared_vecs = lm.score(x_vecs, y)
    return rsquared_vecs, '-', '-'


def evaluate_vecs(vecs_dict, verbose=True):
    results = []
    result, t = predict_ldt(vecs_dict)
    label = 'semantic priming lexical decision RT'
    results.append((label, result, t['duration']))
    if verbose:
        vecs.print_result(label, result, t['duration'])
    result, t = predict_naming(vecs_dict)
    label = 'semantic priming naming RT'
    results.append((label, result, t['duration']))
    if verbose:
        vecs.print_result(label, result, t['duration'])
    return results


if __name__ == '__main__':
    #vecs_fname = '../tmp-jeroen/en.dedup.5pass.d5.t100.vec'
    #vecs_fname = '../pretrained_reference/mkb2017.vec'
    #vecs_fname = '../pretrained_reference/fasttext/crawl-300d-2M.vec'
    vecs_fname = '../pretrained_reference/fasttext/wiki-news-300d-1M-subword.vec'

    argparser = argparse.ArgumentParser(description='predict primed lexical decision and naming response times in Semantic Priming Project data')
    argparser.add_argument('--filename', default=vecs_fname, help='word vectors to evaluate')
    args = argparser.parse_args()

    vecs_dict = vecs.load_vecs(args.filename, normalize=True)
    results = evaluate_vecs(vecs_dict)
