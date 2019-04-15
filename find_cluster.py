import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import vecs
import scipy.spatial.distance

# number of vectors to retrieve from .vec
n_vecs = 1e6

# TODO take word list, retrieve vectors, write to file
def extract_vecs(lang, filename):
    all_vecs = vecs.load_vecs(f'../pretrained/fasttext/cc.{lang}.300.vec', normalize=True, n=n_vecs)
    with open(filename, 'r') as wordlist:
        word_vecs = dict()
        for word in wordlist:
            word = word.strip('\n')
            if ' ' not in word:
                if word in all_vecs.keys():
                    word_vecs[word] = all_vecs[word]
                else:
                    print(f'[WARNING] no vector could be retrieve for \"{word}\"')
            else:
                print(f'[WARNING] \"{word}\" contains spaces, no word vector could be retrieved')
    vecs.write_vecs(word_vecs, f'{lang}_words.vec')


# TODO find cosine distances between these word vectors, plot histogram
def extract_cluster(lang):
    word_vecs = vecs.load_vecs(f'{lang}_words.vec')
    cos_between = dict()
    for key1, value1 in word_vecs.items():
        for key2, value2 in word_vecs.items():
            if key1 != key2:
                cos_between[f'{key1} {key2}'] = scipy.spatial.distance.cosine(value1, value2)
    words = list(word_vecs.keys())
    vecs_array = np.vstack(list(word_vecs.values()))
    median = np.median(vecs_array, axis=0)
    cos_from_median = dict()
    for key, value in word_vecs.items():
        cos_from_median[key] = scipy.spatial.distance.cosine(value, median)
    df = pd.DataFrame.from_dict(cos_from_median, orient='index', columns=['cos_from_median']).rename_axis('word').reset_index()

    df.to_csv(f'{lang}_cos_from_median.tsv', sep='\t')
    print(f'min dist to median: {np.min(df["cos_from_median"])}')
    print(f'max dist to median: {np.max(df["cos_from_median"])}')
    g = sns.distplot(df['cos_from_median'])
    g.set(xlim=(0, 1))
    plt.savefig(f'{lang}_cos_from_median_density.pdf')

    df = pd.DataFrame.from_dict(cos_between, orient='index', columns=['cos_between']).rename_axis('word').reset_index()

    df.to_csv(f'{lang}_cos_between.tsv', sep='\t')
    print(f'cosine distance median: {np.median(df["cos_between"])}')
    print(f'cosine distance mean: {np.mean(df["cos_between"])}')
    g = sns.distplot(df['cos_between'])
    g.set(xlim=(0, 1))
    plt.savefig(f'{lang}_cos_between_density.pdf')

    # TODO take max distance (or 95th percentile of distances?) and grab all other vectors in that radius, write to data file

    all_vecs = vecs.load_vecs(f'../pretrained/fasttext/cc.{lang}.300.vec', normalize=True, n=n_vecs)
    cos_median_all = dict()
    for key, value in all_vecs.items():
        cos_median_all[key] = scipy.spatial.distance.cosine(median, value)
    df = pd.DataFrame.from_dict(cos_median_all, orient='index', columns=['cos_from_median']).rename_axis('word').reset_index()

    # sort in descending order of distance
    df = df.sort_values('cos_from_median')

    # check if present in original
    df['target_word'] = df['word'].isin(word_vecs.keys())

    # write to file
    df[0:10000].to_csv(f'{lang}_results.tsv', sep='\t')
    print('done!')


# TODO take new vector subspace and perform some sort of clustering? (should this be multidimensional or based on cosine distances?)
# TODO produce some sort of word model for the initial word list + other words in the space they enclose
# TODO test: does this work better with raw or with normalized word vectors?


if __name__ == '__main__':
    if __name__ == '__main__':
        argparser = argparse.ArgumentParser(description='clean subtitles for training distributional semantics models')
        argparser.add_argument('lang', help='language to clean')
        argparser.add_argument('--extract_vecs', action='store_true')
        argparser.add_argument('--extract_cluster', action='store_true')
        argparser.add_argument('--filename')
        args = argparser.parse_args()

        if args.extract_vecs:
            extract_vecs(args.lang, args.filename)
        elif args.extract_cluster:
            extract_cluster(args.lang)
        else:
            extract_vecs(args.lang, args.filename)
            extract_cluster(args.lang)
