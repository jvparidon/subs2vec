"""Generate plots presented in Van Paridon & Thompson (2019)."""
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('agg')

# sns.set_palette('Set2')  # use MPI for Psycholinguistics type color palette
sns.set_context('paper', font_scale=1.0)


def gather_similarities(folder):
    """Compile all semantic similarities evaluation results.

    :param folder: directory where the results are located
    :return: pandas DataFrame containing all the similarities results
    """
    df = pd.DataFrame()
    for fname in sorted(os.listdir(folder)):
        if fname.endswith('.txt'):
            with open(os.path.join(folder, fname), 'r') as results_file:
                for line in results_file:
                    line = line.strip('\n')
                    if line.endswith('.vec'):
                        src, lang = line.split('.')[0:2]
                    elif ('-rel' in line) or ('-sim' in line):
                        pass
                    else:
                        task, score, n, n_total = line.split('\t')[0:4]
                        if task.endswith('.tsv'):
                            score = np.abs(float(score))
                            corrected_score = score  # score is already corrected
                            task = task.strip('.tsv').replace('-', ' ')
                            # task = task[3:].strip('.tsv').replace('-', ' ')
                            df = df.append({
                                'lang': lang,
                                'source': src,
                                'task': task,
                                'score': score,
                                'corrected score': corrected_score
                            }, ignore_index=True)
    df['label'] = df['task']
    return df


def gather_analogies(folder):
    """Compile all analogies evaluation results.

    :param folder: directory where the results are located
    :return: pandas DataFrame containing all the analogies results
    """
    df = pd.DataFrame()
    for fname in sorted(os.listdir(folder)):
        if fname.endswith('.txt'):
            with open(os.path.join(folder, fname), 'r') as results_file:
                for line in results_file:
                    line = line.strip('\n')
                    if line.endswith('.vec'):
                        src, lang = line.split('.')[0:2]
                    else:
                        task, score, n, n_total = line.split('\t')[0:4]
                        if task.endswith('.txt'):
                            score = np.abs(float(score))
                            corrected_score = score * (float(n) / float(n_total))
                            task = task.strip('.txt').replace('-', ' ')
                            df = df.append({
                                'lang': lang,
                                'source': src,
                                'task': task,
                                'score': score,
                                'corrected score': corrected_score
                            }, ignore_index=True)
    df['label'] = df['task']
    return df


def gather_norms(folder):
    """Compile all lexical norms evaluation results.

    :param folder: directory where the results are located
    :return: pandas DataFrame containing all the lexical norms results
    """
    df = pd.DataFrame(columns=['norm', 'r', 'r-squared', 'task', 'source', 'lang'])
    for fname in sorted(os.listdir(folder)):
        df_temp = pd.read_csv(os.path.join(folder, fname), sep='\t')
        df_temp['task'] = df_temp['source'].apply(lambda x: x.split('/')[-1])
        df_temp['task'] = df_temp['task'].apply(lambda x: f'{x[3:-5]} ({x[-4:]})')
        df_temp['source'] = fname.split('.')[0]
        df_temp['lang'] = fname.split('.')[1]
        df = df.append(df_temp, ignore_index=True)
    df['corrected score'] = df['r-squared']
    df['label'] = df.apply(lambda x: f'{x["lang"]} {x["task"]} {x["norm"]}', axis=1)
    return df


def plot_scores(df, xlabel, legend_y=1.0):
    g = sns.catplot(x='corrected score', y='label', kind='bar', data=df, legend=False,
                    hue='source', hue_order=['cc', 'wiki-sub', 'sub', 'wiki'],
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

    g.set(xlim=(1.2, 0), ylabel=None, xlabel=xlabel)
    g.set(xticks=(0, .2, .4, .6, .8, 1))
    g.ax.yaxis.tick_right()
    # g.ax.axvline(1.0, color='lightgray')
    g.ax.yaxis.set_tick_params(which='major', reset=False, size=0)
    g.despine(left=True)
    g.ax.legend(loc='upper left', bbox_to_anchor=(0, legend_y), frameon=False)
    return g


if __name__ == '__main__':
    # dataframes
    df_analogies = gather_analogies('results')
    print(df_analogies)
    df_analogies.to_csv('analogies.tsv', sep='\t')

    df_similarities = gather_similarities('results')
    print(df_similarities)
    df_similarities.to_csv('similarities.tsv', sep='\t')

    df_norms = gather_norms('results/norms')
    print(df_norms)
    df_norms.to_csv('norms.tsv', sep='\t')

    # df_analogies = pd.read_csv('analogies.tsv', sep='\t').sort_values('label')
    # df_similarities = pd.read_csv('similarities.tsv', sep='\t').sort_values('label')
    # df_norms = pd.read_csv('norms.tsv', sep='\t').sort_values('label')

    # plots
    g_analogies = plot_scores(df_analogies, 'fraction of correct solutions')
    plt.tight_layout()
    plt.savefig('analogies.png', dpi=600)
    plt.clf()

    g_similarities = plot_scores(df_similarities, 'rank correlation', .98)
    plt.tight_layout()
    plt.savefig('similarities.png', dpi=600)
    plt.clf()

    g_norms = plot_scores(df_norms, 'explained variance')
    plt.tight_layout()
    plt.savefig('norms.png', dpi=600)
    plt.clf()

    df_norms1 = df_norms.iloc[range(int(int(len(df_norms) / 4) / 2) * 4)]
    df_norms2 = df_norms.iloc[range(int(int(len(df_norms) / 4) / 2) * 4, len(df_norms))]

    g_norms1 = plot_scores(df_norms1, 'explained variance', .87)
    plt.tight_layout()
    plt.savefig('norms1.png', dpi=600)
    plt.clf()

    g_norms2 = plot_scores(df_norms2, 'explained variance')
    plt.tight_layout()
    plt.savefig('norms2.png', dpi=600)
    plt.clf()
