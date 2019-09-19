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
# sns.set_palette('Set2')  # use MPI for Psycholinguistics type color palette


def gather_similarities(folder):
    """Compile all semantic similarities evaluation results.

    :param folder: directory where the results are located
    :return: pandas DataFrame containing all the similarities results
    """
    df = pd.DataFrame(columns=['rank r', 'adjusted rank r', 'vecs', 'source', 'lang'])
    for fname in sorted(os.listdir(folder)):
        df_temp = pd.read_csv(os.path.join(folder, fname), sep='\t')

        df_temp['source'] = df_temp['source'].apply(lambda x: ' '.join(x.split("-")[1:]))
        df_temp['source'] = df_temp['source'].str.replace('.tsv', '')

        df_temp['vecs'] = fname.split('.')[0]
        df_temp['vecs'] = df_temp['vecs'].str.replace('cc', 'fasttext').replace('wiki-subs', 'wiki+subs')

        df_temp['lang'] = fname.split('.')[1]
        df = df.append(df_temp, ignore_index=True)

    df['label'] = df.apply(lambda x: f'{x["lang"]} {x["source"]}', axis=1)
    df = df.loc[df['source'].apply(lambda x: False if x.endswith('rel') else True)]
    df = df.loc[df['source'].apply(lambda x: False if x.endswith('no') else True)]
    df = df.loc[df['label'].apply(lambda x: x != 'en wordsim353 all')]
    df['label'] = df['label'].str.replace(' sim', ' all')
    df['label'] = df['label'].str.replace(' all', '')
    df = df.sort_values(['label', 'vecs'])
    return df


def gather_analogies(folder):
    """Compile all analogies evaluation results.

    :param folder: directory where the results are located
    :return: pandas DataFrame containing all the analogies results
    """
    df = pd.DataFrame(columns=['score', 'adjusted score', 'vecs', 'source', 'lang'])
    for fname in sorted(os.listdir(folder)):
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

    df['label'] = df.apply(lambda x: f'{x["lang"]} {x["source"]}', axis=1)
    df = df.loc[df['lang'] != 'hi']
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
        df_temp = pd.read_csv(os.path.join(folder, fname), sep='\t')

        df_temp['source'] = df_temp['source'].str.replace('.tsv', '')
        df_temp['source'] = df_temp['source'].apply(lambda x: f'{"-".join(x.split("-")[1:-1])} ({x.split("-")[-1]})')

        df_temp['vecs'] = fname.split('.')[0]
        df_temp['vecs'] = df_temp['vecs'].str.replace('cc', 'fasttext').replace('wiki-subs', 'wiki+subs')

        df_temp['lang'] = fname.split('.')[1]

        df = df.append(df_temp, ignore_index=True)
    df['label'] = df.apply(lambda x: f'{x["lang"]} {x["source"]} {x["norm"]}', axis=1)
    df = df.sort_values(['label', 'vecs'])
    return df


def plot_scores(df, xlabel, legend_y=1.0):
    g = sns.catplot(x=xlabel, y='label', kind='bar', data=df, legend=False,
                    hue='vecs', hue_order=['fasttext', 'wiki+subs', 'subs', 'wiki'],
                    height=len(df) / 12,
                    aspect=1 / np.log10(len(df)))

    '''
    # draw vlines
    langs = df.groupby('lang').count()[['score']]
    tasks = df.groupby('task').count()[['score']]
    lines = np.cumsum(langs['score'])
    end = lines[-1]
    for line in lines[:-1]:
        pos = (line / end) * len(tasks)
        g.ax.axhline(pos - .5, color='black')
    '''

    # g = sns.FacetGrid(df, row='lang', sharey=False, sharex=True, margin_titles=True)
    # g.map_dataframe(sns.barplot, x='corrected score', y='task', hue='source', palette='Set2')
    # g.map(plt.barh, width='corrected score', y='task', height=1)

    g.set(xticks=(0, .2, .4, .6, .8, 1))
    g.ax.yaxis.tick_right()
    # g.ax.axvline(1.0, color='lightgray')
    #g.ax.yaxis.set_tick_params(which='major', reset=False, size=0)

    g.despine(left=True, right=False)
    g.set(xlim=(1.1, 0), ylabel=None)  # , xlabel=xlabel)
    #g.ax.legend(loc='upper left', bbox_to_anchor=(-0.05, legend_y), frameon=False)
    g.ax.legend(loc='upper left', bbox_to_anchor=(0, legend_y), frameon=False)
    return g


if __name__ == '__main__':
    # dataframes
    df_analogies = gather_analogies(os.path.join(path, 'paper_results', 'analogies'))
    #print(df_analogies.head())
    df_analogies.to_csv('analogies.tsv', sep='\t')

    df_similarities = gather_similarities(os.path.join(path, 'paper_results', 'similarities'))
    #print(df_similarities.head())
    df_similarities.to_csv('similarities.tsv', sep='\t')

    df_norms = gather_norms(os.path.join(path, 'paper_results', 'norms'))
    #print(df_norms.head())
    df_norms.to_csv('norms.tsv', sep='\t')

    # df_analogies = pd.read_csv('analogies.tsv', sep='\t').sort_values('label')
    # df_similarities = pd.read_csv('similarities.tsv', sep='\t').sort_values('label')
    # df_norms = pd.read_csv('norms.tsv', sep='\t').sort_values('label')

    # plots
    g_analogies = plot_scores(df_analogies, 'adjusted score', .48)
    plt.tight_layout()
    plt.savefig('analogies.png', dpi=600)
    plt.clf()

    g_similarities = plot_scores(df_similarities, 'adjusted rank r', .48)
    plt.tight_layout()
    plt.savefig('similarities.png', dpi=600)
    plt.clf()

    #g_norms = plot_scores(df_norms, 'adjusted r')
    #plt.tight_layout()
    #plt.savefig('norms.png', dpi=600)
    #plt.clf()

    df_norms1 = df_norms.iloc[range(int(int(len(df_norms) / 4) / 2) * 4)]
    df_norms2 = df_norms.iloc[range(int(int(len(df_norms) / 4) / 2) * 4, len(df_norms))]

    g_norms1 = plot_scores(df_norms1, 'adjusted r', .495)
    plt.tight_layout()
    plt.savefig('norms1.png', dpi=600)
    plt.clf()

    g_norms2 = plot_scores(df_norms2, 'adjusted r', .55)
    plt.tight_layout()
    plt.savefig('norms2.png', dpi=600)
    plt.clf()
