"""Generate plots presented in Van Paridon & Thompson (2019)."""
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('agg')
path = os.path.dirname(__file__)

sns.set(context='paper', style='whitegrid', font_scale=1.0, rc={'grid.color': '.9', 'grid.linewidth': '.5'})
sns.set_palette('Set2')  # use MPI for Psycholinguistics type color palette


def add_wordcounts(df):
    wordcounts = {
        'af': {
            'subs': 323000,
            'wiki': 17000000
        },
        'ar': {
            'subs': 188000000,
            'wiki': 119000000
        },
        'bg': {
            'subs': 246000000,
            'wiki': 53000000
        },
        'bn': {
            'subs': 2227000,
            'wiki': 18000000
        },
        'br': {
            'subs': 110000,
            'wiki': 7644000
        },
        'bs': {
            'subs': 91000000,
            'wiki': 13000000
        },
        'ca': {
            'subs': 3098000,
            'wiki': 175000000
        },
        'cs': {
            'subs': 249000000,
            'wiki': 100000000
        },
        'da': {
            'subs': 87000000,
            'wiki': 56000000
        },
        'de': {
            'subs': 139000000,
            'wiki': 976000000
        },
        'el': {
            'subs': 271000000,
            'wiki': 58000000
        },
        'en': {
            'subs': 750000000,
            'wiki': 2477000000
        },
        'eo': {
            'subs': 381000,
            'wiki': 37000000
        },
        'es': {
            'subs': 514000000,
            'wiki': 585000000
        },
        'et': {
            'subs': 60000000,
            'wiki': 29000000
        },
        'eu': {
            'subs': 3400000,
            'wiki': 20000000
        },
        'fa': {
            'subs': 45000000,
            'wiki': 86000000
        },
        'fi': {
            'subs': 116000000,
            'wiki': 73000000
        },
        'fr': {
            'subs': 335000000,
            'wiki': 724000000
        },
        'gl': {
            'subs': 1666000,
            'wiki': 40000000
        },
        'he': {
            'subs': 169000000,
            'wiki': 132000000
        },
        'hi': {
            'subs': 695000,
            'wiki': 31000000
        },
        'hr': {
            'subs': 241000000,
            'wiki': 42000000
        },
        'hu': {
            'subs': 227000000,
            'wiki': 120000000
        },
        'hy': {
            'subs': 23000,
            'wiki': 38000000
        },
        'id': {
            'subs': 65000000,
            'wiki': 69000000
        },
        'is': {
            'subs': 7474000,
            'wiki': 7196000
        },
        'it': {
            'subs': 277000000,
            'wiki': 476000000
        },
        'ka': {
            'subs': 1108000,
            'wiki': 15000000
        },
        'kk': {
            'subs': 13000,
            'wiki': 18000000
        },
        'ko': {
            'subs': 6834000,
            'wiki': 62000000
        },
        'lt': {
            'subs': 6252000,
            'wiki': 23000000
        },
        'lv': {
            'subs': 2167000,
            'wiki': 13000000
        },
        'mk': {
            'subs': 20000000,
            'wiki': 26000000
        },
        'ml': {
            'subs': 1520000,
            'wiki': 10000000
        },
        'ms': {
            'subs': 12000000,
            'wiki': 28000000
        },
        'nl': {
            'subs': 264000000,
            'wiki': 248000000
        },
        'no': {
            'subs': 45000000,
            'wiki': 90000000
        },
        'pl': {
            'subs': 250000000,
            'wiki': 232000000
        },
        'pt': {
            'subs': 257000000,
            'wiki': 238000000
        },
        'ro': {
            'subs': 434000000,
            'wiki': 65000000
        },
        'ru': {
            'subs': 152000000,
            'wiki': 390000000
        },
        'si': {
            'subs': 3493000,
            'wiki': 5980000
        },
        'sk': {
            'subs': 47000000,
            'wiki': 28000000
        },
        'sl': {
            'subs': 106000000,
            'wiki': 31000000
        },
        'sq': {
            'subs': 11000000,
            'wiki': 17000000
        },
        'sr': {
            'subs': 343000000,
            'wiki': 69000000
        },
        'sv': {
            'subs': 101000000,
            'wiki': 143000000
        },
        'ta': {
            'subs': 123000,
            'wiki': 17000000
        },
        'te': {
            'subs': 103000,
            'wiki': 15000000
        },
        'tl': {
            'subs': 87000,
            'wiki': 6515000
        },
        'tr': {
            'subs': 239000000,
            'wiki': 54000000
        },
        'uk': {
            'subs': 4945000,
            'wiki': 162000000
        },
        'ur': {
            'subs': 195000,
            'wiki': 15000000
        },
        'vi': {
            'subs': 27000000,
            'wiki': 115000000
        }
    }
    df['wordcount'] = df.apply(lambda x: wordcounts[x['lang']].get(x['vecs'], np.nan), axis=1)
    return df


def replace_iso(series):
    labels = {
        'ar': 'arabic',
        'cs': 'czech',
        'de': 'german',
        'el': 'greek',
        'en': 'english',
        'es': 'spanish',
        'fa': 'farsi',
        'fi': 'finnish',
        'fr': 'french',
        'he': 'hebrew',
        'hi': 'hindi',
        'id': 'indonesian',
        'it': 'italian',
        'ms': 'malay',
        'nl': 'dutch',
        'pl': 'polish',
        'pt': 'portuguese',
        'ro': 'romanian',
        'ru': 'russian',
    }
    for lang, language in labels.items():
        series = series.str.replace(lang, language)
    return series


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

    df['language'] = replace_iso(df['lang'])
    df['label'] = df.apply(lambda x: f'{x["language"]}: {x["source"]}', axis=1)
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

    df['language'] = replace_iso(df['lang'])
    df['label'] = df.apply(lambda x: f'{x["language"]}: {x["source"]}', axis=1)
    #df = df.loc[df['lang'] != 'hi']
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
    df_norms['language'] = replace_iso(df_norms['lang'])
    df_norms['label'] = df_norms.apply(lambda x: f'{x["language"]}: {x["source"]} {x["norm"]}', axis=1)
    df_norms = df_norms.sort_values(['label', 'vecs'])

    df_binder = df.loc[df['source'] == 'binder (2016)'].copy()
    df_binder = df_binder.loc[(df_binder['norm'] != 'mean r') & (df_binder['norm'] != 'word length')]
    df_binder['label'] = df_binder['norm']
    df_binder = df_binder.sort_values(['label', 'vecs'])

    return df_norms, df_binder


def plot_scores(df, xlabel, aspect=.5, legend_y=1.0):
    g = sns.catplot(x=xlabel, y='label', kind='bar', data=df, legend=False,
                    hue='vecs', hue_order=['wiki+subs', 'subs', 'wiki'],
                    height=len(df) / 12,
                    # aspect=1 / np.log10(len(df))
                    aspect=aspect,
                    )

    g.set(xticks=(0, .2, .4, .6, .8, 1))
    g.ax.yaxis.tick_right()

    g.despine(left=True, right=False)
    g.set(xlim=(1.1, 0), ylabel=None)  # , xlabel=xlabel)
    g.ax.legend(loc='upper left', bbox_to_anchor=(-0.05, legend_y), frameon=False)
    # g.ax.legend(loc='upper left', bbox_to_anchor=(0, legend_y), frameon=False)
    return g


def plot_wordcounts(df):
    df_means = df.groupby(['lang', 'vecs', 'kind'], as_index=False).mean()
    df_means['log10 wordcount'] = np.log10(df_means['wordcount'])
    df_means['wordcount-adjusted score'] = df_means['score'] / df_means['log10 wordcount']
    '''
    g = sns.lmplot(y='wordcount-adjusted score', x='log10 wordcount', hue='vecs',
                   row='kind', sharex=True, legend=False,
                   data=df_means, aspect=2, height=3,
                   )
    ylabels = ['mean analogies score per language', 'mean similarities score per language', 'mean norms score per language']
    for i in range(len(ylabels)):
        g.axes[i][0].set(ylabel=ylabels[i])
    #g.set(ylim=(-0.1, 1.1), xlim=(7, 9.5), title='')
    g.axes[2][0].legend(loc='lower right', frameon=False)
    '''
    '''
    g = sns.catplot(y='wordcount-adjusted score', hue='vecs', hue_order=['subs', 'wiki'], x='kind',
                    kind='violin', data=df_means, legend=False, inner='quartile', cut=0, split=True, aspect=.7)
    g.ax.legend(loc='lower right', frameon=False)
    g.set(ylim=(0, None), xlabel='')
    '''
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
    # dataframes
    df_analogies = gather_analogies(os.path.join(path, 'paper_results', 'analogies'))
    df_analogies.to_csv('analogies.tsv', sep='\t')

    df_similarities = gather_similarities(os.path.join(path, 'paper_results', 'similarities'))
    df_similarities.to_csv('similarities.tsv', sep='\t')

    df_norms, df_binder = gather_norms(os.path.join(path, 'paper_results', 'norms'))
    df_norms.to_csv('norms.tsv', sep='\t')
    df_binder.to_csv('binder.tsv', sep='\t')

    # df_analogies = pd.read_csv('analogies.tsv', sep='\t').sort_values('label')
    # df_similarities = pd.read_csv('similarities.tsv', sep='\t').sort_values('label')
    # df_norms = pd.read_csv('norms.tsv', sep='\t').sort_values('label')

    # plots
    g_analogies = plot_scores(df_analogies, 'adjusted score', .7, .45)
    plt.tight_layout()
    plt.savefig('analogies.pdf')
    plt.savefig('analogies.png', dpi=600)
    plt.clf()

    g_similarities = plot_scores(df_similarities, 'adjusted rank r', .5, .30)
    plt.tight_layout()
    plt.savefig('similarities.pdf')
    plt.savefig('similarities.png', dpi=600)
    plt.clf()

    df_norms1 = df_norms.iloc[range(int(int(len(df_norms) / 3) / 2) * 3)]
    df_norms2 = df_norms.iloc[range(int(int(len(df_norms) / 3) / 2) * 3, len(df_norms))]

    df_binder1 = df_binder.iloc[range(int(int(len(df_binder) / 3) / 2) * 3)]
    df_binder2 = df_binder.iloc[range(int(int(len(df_binder) / 3) / 2) * 3, len(df_binder))]

    g_norms1 = plot_scores(df_norms1, 'adjusted r', .7, .125)
    plt.tight_layout()
    plt.savefig('norms1.pdf')
    plt.savefig('norms1.png', dpi=600)
    plt.clf()

    g_norms2 = plot_scores(df_norms2, 'adjusted r', .7, .625)
    plt.tight_layout()
    plt.savefig('norms2.pdf')
    plt.savefig('norms2.png', dpi=600)
    plt.clf()

    g_binder1 = plot_scores(df_binder1, 'adjusted r', .5, .55)
    plt.tight_layout()
    plt.savefig('binder1.pdf')
    plt.savefig('binder1.png', dpi=600)
    plt.clf()

    g_binder2 = plot_scores(df_binder2, 'adjusted r', .5, .9)
    plt.tight_layout()
    plt.savefig('binder2.pdf')
    plt.savefig('binder2.png', dpi=600)
    plt.clf()

    # scatter
    df_a = df_analogies[['lang', 'source', 'vecs', 'adjusted score']].rename(columns={'adjusted score': 'score'})
    df_s = df_similarities[['lang', 'source', 'vecs', 'adjusted rank r']].rename(columns={'adjusted rank r': 'score'})
    df_n = df_norms[['lang', 'source', 'vecs', 'adjusted r']].rename(columns={'adjusted r': 'score'})
    df_a['kind'] = 'analogies'
    df_s['kind'] = 'similarities'
    df_n['kind'] = 'norms'

    df_wordcounts = pd.concat([df_a, df_s, df_n])
    df_wordcounts = add_wordcounts(df_wordcounts).dropna()
    g_wordcounts = plot_wordcounts(df_wordcounts)
    plt.tight_layout()
    plt.savefig('wordcounts.pdf')
    plt.savefig('wordcounts.png', dpi=600)
    plt.clf()
