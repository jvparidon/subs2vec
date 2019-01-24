import numpy as np
import vecs
import sklearn.decomposition


def pca_subs(subvecs, n_components=2):
    sub2pca = {}
    pca = sklearn.decomposition.PCA(n_components=n_components)

    # decompose and save eigenvectors, eigenvalues, means
    pca.fit(subvecs)
    sub2pca['eigenvectors'] = np.transpose(pca.components_)
    sub2pca['eigenvalues'] = pca.explained_variance_
    sub2pca['explained_variance'] = pca.explained_variance_ratio_
    sub2pca['means'] = pca.mean_
    return sub2pca


if __name__ == '__main__':
    '''
    fname = '../tmp-jeroen/en.dedup.5pass.d5.t100.vec'
    vecs_dict = vecs.load_vecs(fname, n=1e6, d=300)
    vecs_array = np.vstack(list(vecs_dict.values()))
    sub2pca = pca_subs(vecs_array, n_components=300)
    for key, array in sub2pca.items():
        np.savetxt(fname.replace('.vec', '.{}'.format(key)), array)
    '''

    fname = '../tmp-jeroen/en.dedup.5pass.d5.t100.vec'
    #fname = '../pretrained/binder.vec'
    #fname = '../pretrained/fasttext/wiki-news-300d-1M-subword.vec'
    #fname = '../pretrained/glove.840B.300d.vec'
    vecs_dict = vecs.load_vecs(fname, n=1e6, d=300)
    vecs_array = np.vstack(list(vecs_dict.values()))
    sub2pca = pca_subs(vecs_array, n_components=65)
    for key, array in sub2pca.items():
        np.savetxt(fname.replace('.vec', '.65d.{}'.format(key)), array)
