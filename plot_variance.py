import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import math
import sklearn.decomposition


def pca_normal(shape=(int(1e6), 300)):
    noise = np.random.normal(size=shape)
    pca = sklearn.decomposition.PCA(n_components=shape[1])
    pca.fit(noise)
    return pca.explained_variance_ratio_


def plot_variance(fnames):
    plt.clf()
    sns.set_style('darkgrid')
    sns.set_context('notebook', rc={'lines.linewidth': 2.5})
    plt.figure(figsize=(12, 8))
    for i in range(len(fnames)):
        vecs = np.loadtxt(fnames[i])
        fname = fnames[i].replace('.explained_variance', '').split('/')[-1]
        plt.plot(np.hstack([0.0, np.cumsum(vecs)]), alpha=.5, label='{}'.format(fname))
    #plt.plot(np.hstack([0.0, np.cumsum(pca_normal((3000, 300)))]), alpha=.5, label='Gaussian noise (3k samples)')
    plt.plot(np.hstack([0.0, np.cumsum(pca_normal())]), alpha=.5, label='Gaussian noise')
    x = np.array(range(300)) / 300
    plt.plot(np.power(x, 1 / math.e), alpha=.5, label=r'$y = x^{1/e}$')
    x = np.array(range(65)) / 65
    plt.plot(np.power(x, 1 / math.e), alpha=.5, label=r'$y = x^{1/e}$')
    #plt.plot(x, alpha=.5, label=r'$y = x$')
    plt.legend()
    plt.ylim((-.1, 1.1))
    plt.ylabel('cumulative R-squared')
    plt.xlabel('dimensions')
    plt.title('explained variance in 300d word vector PCA')
    plt.savefig('300d_pca.png', dpi=100)


if __name__ == '__main__':
    #fnames = ['en.dedup.5pass.d5.t100.3000d.explained_variance']
    fnames = ['../pretrained/fasttext/wiki-news-300d-1M-subword.reduced.explained_variance',
              '../pretrained/glove.840B.300d.explained_variance',
              '../tmp-jeroen/en.dedup.5pass.d5.t100.shuffled.explained_variance',
              '../tmp-jeroen/en.dedup.5pass.d5.t100.explained_variance',
              #'../tmp-jeroen/en.dedup.5pass.d5.t100.minus_top10k.explained_variance',
              '../tmp-jeroen/en.dedup.5pass.d5.t100.minus_top100k.explained_variance',
              '../tmp-jeroen/nl.dedup.5pass.d5.t100.explained_variance',
              '../tmp-jeroen/de.dedup.5pass.d5.t100.explained_variance',
              '../tmp-jeroen/fa.dedup.5pass.d5.t100.explained_variance',
              '../pretrained/binder.explained_variance',
              ]
    plot_variance(fnames)
