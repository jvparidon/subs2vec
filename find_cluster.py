import argparse
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import vecs
import scipy.spatial.distance


# TODO take word list, retrieve vectors, write to file
def extract_vecs(lang, filename):
    all_vecs = vecs.load_vecs(f'../pretrained/fasttext/cc.{lang}.vec', normalize=True, n=1e5)
    with open(filename, 'r') as wordlist:
        word_vecs = dict()
        for word in wordlist:
            word = word.strip('\n')
            word_vecs[word] = all_vecs.get(word, np.nan)
    vecs.write_vecs(word_vecs, f'{lang}_words.vec')


# TODO find cosine distances between these word vectors, plot histogram
def cluster(lang):
    word_vecs = vecs.load_vecs(f'{lang}_words.vec')
    cossims = dict()
    for key1, value1 in word_vecs:
        for key2, value2 in word_vecs:
            if key1 != key2:
                cossims[f'{key1} {key2}'] = scipy.spatial.distance.cosine(value1, value2)
    vecs.write_vecs(cossims, f'{lang}_cossims.vec')
    cossims_values = cossims.values()
    print(f'cosine distance median: {np.median(cossims_values)}')
    print(f'cosine distance mean: {np.mean(cossims_values)}')
    sns.distplot(list(cossims_values))
    plt.savefig('cosine_dist.pdf')


# TODO take max distance (or 95th percentile of distances?) and grab all other vectors in that radius, write to data file
def extract_cluster(lang, filename):
    pass


# TODO take new vector subspace and perform some sort of clustering? (should this be multidimensional or based on cosine distances?)
# TODO produce some sort of word model for the initial word list + other words in the space they enclose
# TODO test: does this work better with raw or with normalized word vectors?


if __name__ == '__main__':
    if __name__ == '__main__':
        argparser = argparse.ArgumentParser(description='clean subtitles for training distributional semantics models')
        argparser.add_argument('lang', help='language to clean')
        argparser.add_argument('--extract_vecs', action='store_true')
        argparser.add_argument('--cluster', action='store_true')
        argparser.add_argument('--extract_cluster', action='store_true')
        argparser.add_argument('--filename')
        args = argparser.parse_args()

        if args.extract_vecs:
            extract_vecs(args.lang, args.filename)
        elif args.cluster:
            cluster(args.lang)
        elif args.extract_cluster:
            extract_cluster(args.lang, args.filename)
