"""Compile embedding evaluation stats and generate plots as presented in Van Paridon & Thompson (2020)."""
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
path = os.path.dirname(__file__)
df_corpus = pd.read_csv(os.path.join(path, 'paper_results', 'table_data.tsv'), sep='\t')

sns.set(context='paper', style='whitegrid', font_scale=1.0, rc={'grid.color': '.9', 'grid.linewidth': '.5'})
sns.set_palette('Set2')  # use MPI for Psycholinguistics style color palette


def gather_similarities(folder):
    """Compile all semantic similarities evaluation results.

    :param folder: directory where the results are located
    :return: pandas DataFrame containing all the similarities results
    """
    df = pd.DataFrame(columns=['rank r', 'adjusted rank r', 'vecs', 'source', 'lang'])
    for fname in sorted(os.listdir(folder)):
        if not fname.startswith('cc'):
            df_temp = pd.read_csv(os.path.join(folder, fname), sep='\t')

            df_temp['source'] = df_temp['source'].apply(lambda x: ' '.join(x.split("-")[1:]))
            df_temp['source'] = df_temp['source'].str.replace('.tsv', '')

            df_temp['vecs'] = fname.split('.')[0]
            df_temp['vecs'] = df_temp['vecs'].str.replace('cc', 'fasttext').replace('wiki-subs', 'wiki+subs')

            df_temp['lang'] = fname.split('.')[1]
            df = df.append(df_temp, ignore_index=True)

    df = df.loc[df['source'].apply(lambda x: False if x.endswith('rel') else True)]
    df = df.loc[df['source'].apply(lambda x: False if x.endswith('no') else True)]
    df = df.loc[(df['lang'] != 'en') | (df['source'] != 'wordsim353 all')]
    df['source'] = df['source'].str.replace(' sim', '')
    df['source'] = df['source'].str.replace(' all', '')

    df = df.merge(df_corpus[['lang', 'vecs', 'language']], how='left', on=['lang', 'vecs'])
    df['label'] = df.apply(lambda x: f'{x["language"]}: {x["source"]}'.lower(), axis=1)
    df = df.sort_values(['label', 'vecs'])
    return df


def gather_analogies(folder):
    """Compile all analogies evaluation results.

    :param folder: directory where the results are located
    :return: pandas DataFrame containing all the analogies results
    """
    df = pd.DataFrame(columns=['score', 'adjusted score', 'vecs', 'source', 'lang'])
    for fname in sorted(os.listdir(folder)):
        if not fname.startswith('cc'):
            df_temp = pd.read_csv(os.path.join(folder, fname), sep='\t')

            df_temp['source'] = df_temp['source'].apply(lambda x: ' '.join(x.split("-")[1:]))
            df_temp['source'] = df_temp['source'].str.replace('.tsv', '')
            df_temp['source'] = df_temp['source'].str.replace('_nocountries', ' (no geo)')
            df_temp['source'] = df_temp['source'].str.replace('_no_countries', ' (no geo)')
            df_temp['source'] = df_temp['source'].str.replace(' google', '')

            df_temp['vecs'] = fname.split('.')[0]
            df_temp['vecs'] = df_temp['vecs'].str.replace('cc', 'fasttext').replace('wiki-subs', 'wiki+subs')

            df_temp['lang'] = fname.split('.')[1]
            df = df.append(df_temp, ignore_index=True)

    df = df.merge(df_corpus[['lang', 'vecs', 'language']], how='left', on=['lang', 'vecs'])
    df['label'] = df.apply(lambda x: f'{x["language"]}: {x["source"]}'.lower(), axis=1)
    df = df.loc[df['source'].apply(lambda x: False if x.endswith('semrel') else True)]
    df = df.loc[df['source'].apply(lambda x: False if x.endswith('bless') else True)]
    df = df.sort_values(['label', 'vecs'])
    return df


def gather_norms(folder):
    """Compile all lexical norms evaluation results.

    :param folder: directory where the results are located
    :return: pandas DataFrame containing all the lexical norms results
    """
    df = pd.DataFrame(columns=['norm', 'adjusted r', 'adjusted r-squared', 'r-squared', 'vecs', 'source', 'lang'])
    for fname in sorted(os.listdir(folder)):
        if not fname.startswith('cc'):
            df_temp = pd.read_csv(os.path.join(folder, fname), sep='\t')

            df_temp['source'] = df_temp['source'].str.replace('.tsv', '')
            df_temp['source'] = df_temp['source'].apply(lambda x: f'{"-".join(x.split("-")[1:-1])} ({x.split("-")[-1]})')

            df_temp['vecs'] = fname.split('.')[0]
            df_temp['vecs'] = df_temp['vecs'].str.replace('cc', 'fasttext').replace('wiki-subs', 'wiki+subs')

            df_temp['lang'] = fname.split('.')[1]

            df = df.append(df_temp, ignore_index=True)

    df_norms = df.loc[df['source'] != 'binder (2016)'].copy()
    df_norms = df_norms.merge(df_corpus[['lang', 'vecs', 'language']], how='left', on=['lang', 'vecs'])
    df_norms['label'] = df_norms.apply(lambda x: f'{x["language"]}: {x["source"]} {x["norm"]}'.lower(), axis=1)
    df_norms = df_norms.sort_values(['label', 'vecs'])

    df_binder = df.loc[df['source'] == 'binder (2016)'].copy()
    df_binder = df_binder.loc[(df_binder['norm'] != 'mean r') & (df_binder['norm'] != 'word length')]
    df_binder['label'] = df_binder['norm']
    df_binder = df_binder.sort_values(['label', 'vecs'])

    return df_norms, df_binder


def _plot_scores(df, xlabel, aspect=.5):
    g = sns.catplot(x=xlabel, y='label', kind='bar', data=df, legend=False,
                    hue='vecs', hue_order=['wiki+subs', 'subs', 'wiki'],
                    height=len(df) / 12, aspect=aspect
                    )

    g.set(xticks=(0, .2, .4, .6, .8, 1))
    g.ax.yaxis.tick_right()

    g.despine(left=True, right=False)
    g.set(xlim=(1.1, 0), ylabel=None)
    g.ax.legend(loc='upper left', bbox_to_anchor=(1.1, 0), frameon=False)
    return g


def _plot_wordcounts(df):
    df_means = df.groupby(['lang', 'vecs', 'kind'], as_index=False).mean()
    df_means['log10 wordcount'] = np.log10(df_means['words'])
    df_means['wordcount-adjusted score'] = df_means['score'] / df_means['log10 wordcount']
    df_subs = df_means.loc[df_means['vecs'] == 'subs'].rename(columns={'wordcount-adjusted score': 'wordcount-adjusted score for subtitle vectors'}).reset_index()
    df_wiki = df_means.loc[df_means['vecs'] == 'wiki'].rename(columns={'wordcount-adjusted score': 'wordcount-adjusted score for wikipedia vectors'}).reset_index()
    df_means = df_subs
    df_means['wordcount-adjusted score for wikipedia vectors'] = df_wiki['wordcount-adjusted score for wikipedia vectors']
    g = sns.relplot(kind='scatter', data=df_means, hue='kind',
                    x='wordcount-adjusted score for wikipedia vectors', y='wordcount-adjusted score for subtitle vectors',
                    height=4, aspect=.8,
                    )

    g._legend.remove()
    g.ax.legend(loc='lower right', frameon=False)
    g.ax.legend_.texts[0].set_text('')

    g.ax.plot([0, .11], [0, .11], linestyle='--', color='lightgray')
    g.set(xlim=(0, .11), ylim=(0, .11))
    return g


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='generate plots from the subs2vec paper')
    argparser.add_argument('--unadjusted', action='store_true', help='generate plots from scores not adjusted for missing data')
    args = argparser.parse_args()
    if args.unadjusted:
        prefix = ''
    else:
        prefix = 'adjusted '

    # create dataframes
    df_analogies = gather_analogies(os.path.join(path, 'paper_results', 'analogies'))
    df_analogies.to_csv('analogies.tsv', sep='\t', index=False)

    df_similarities = gather_similarities(os.path.join(path, 'paper_results', 'similarities'))
    df_similarities.to_csv('similarities.tsv', sep='\t', index=False)

    df_norms, df_binder = gather_norms(os.path.join(path, 'paper_results', 'norms'))
    df_norms.to_csv('norms.tsv', sep='\t', index=False)
    df_binder.to_csv('binder.tsv', sep='\t', index=False)

    # cut norms and binder dataframes up so the plots will fit on a page
    chunk = int(len(df_norms) / 12)
    df_norms1 = df_norms.iloc[range(chunk * 3)]
    df_norms2 = df_norms.iloc[range(chunk * 3, chunk * 6)]
    df_norms3 = df_norms.iloc[range(chunk * 6, chunk * 9)]
    df_norms4 = df_norms.iloc[range(chunk * 9, len(df_norms))]

    df_binder1 = df_binder.iloc[range(int(int(len(df_binder) / 3) / 2) * 3)]
    df_binder2 = df_binder.iloc[range(int(int(len(df_binder) / 3) / 2) * 3, len(df_binder))]

    # draw barplots
    g_analogies = _plot_scores(df_analogies, f'{prefix}score', .7)
    plt.tight_layout()
    plt.savefig('analogies.pdf')
    plt.savefig('analogies.png', dpi=600)
    plt.clf()

    g_similarities = _plot_scores(df_similarities, f'{prefix}rank r', .5)
    plt.tight_layout()
    plt.savefig('similarities.pdf')
    plt.savefig('similarities.png', dpi=600)
    plt.clf()

    g_norms1 = _plot_scores(df_norms1, f'{prefix}r', .5)
    plt.tight_layout()
    plt.savefig('norms1.pdf')
    plt.savefig('norms1.png', dpi=600)
    plt.clf()

    g_norms2 = _plot_scores(df_norms2, f'{prefix}r', .5)
    plt.tight_layout()
    plt.savefig('norms2.pdf')
    plt.savefig('norms2.png', dpi=600)
    plt.clf()

    g_norms3 = _plot_scores(df_norms3, f'{prefix}r', .5)
    plt.tight_layout()
    plt.savefig('norms3.pdf')
    plt.savefig('norms3.png', dpi=600)
    plt.clf()

    g_norms4 = _plot_scores(df_norms4, f'{prefix}r', .5)
    plt.tight_layout()
    plt.savefig('norms4.pdf')
    plt.savefig('norms4.png', dpi=600)
    plt.clf()

    g_binder1 = _plot_scores(df_binder1, f'{prefix}r', .5)
    plt.tight_layout()
    plt.savefig('binder1.pdf')
    plt.savefig('binder1.png', dpi=600)
    plt.clf()

    g_binder2 = _plot_scores(df_binder2, f'{prefix}r', .5)
    plt.tight_layout()
    plt.savefig('binder2.pdf')
    plt.savefig('binder2.png', dpi=600)
    plt.clf()

    if not args.unadjusted:
        # draw scatterplot
        df_a = df_analogies[['lang', 'source', 'vecs', 'adjusted score']].rename(columns={'adjusted score': 'score'})
        df_s = df_similarities[['lang', 'source', 'vecs', 'adjusted rank r']].rename(columns={'adjusted rank r': 'score'})
        df_n = df_norms[['lang', 'source', 'vecs', 'adjusted r']].rename(columns={'adjusted r': 'score'})
        df_a['kind'] = 'analogies'
        df_s['kind'] = 'similarities'
        df_n['kind'] = 'norms'

        df_wordcounts = pd.concat([df_a, df_s, df_n])
        df_wordcounts = df_wordcounts.merge(df_corpus[['lang', 'vecs', 'words']], how='inner', on=['lang', 'vecs'])
        df_wordcounts.to_csv('model_data.tsv', sep='\t', index=False)

        sns.set_palette(sns.color_palette('Set2')[3:])  # skip the first three colors, because we use those to label training corpus
        g_wordcounts = _plot_wordcounts(df_wordcounts.dropna())
        plt.tight_layout()
        plt.savefig('wordcounts.pdf')
        plt.savefig('wordcounts.png', dpi=600)
        plt.clf()
