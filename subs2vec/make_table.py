"""Generate tables from Van Paridon & Thompson (2020)."""
import pandas as pd
import argparse
import os
path = os.path.dirname(__file__)


def parse_big_number(num):
    """Parse large numbers into human readable format (e.g., 1K, 1M, 1B).

    :param num: int or float of number to parse
    :return: str of parsed number
    """
    if num < 1e3:
        num = f'{num}'
    elif num < 1e6:
        num = f'{num / 1e3:.0f}K'
    elif num < 1e9:
        num = f'{num / 1e6:.0f}M'
    else:
        num = f'{num / 1e9:.0f}B'
    return num


def _vec_links(row):
    topvecs = f"[top 1M vectors]({row['topvecs']}@download)"
    allvecs = f"[all vectors]({row['allvecs']}@download)"
    binary = f"[model binary]({row['binary']}@download)"
    return f'{topvecs}<br>{allvecs}<br>{binary}'


def _freq_links(row):
    wordfreq = f"[word counts]({row['wordfreq']}@download)"
    bigramfreq = f"[bigram counts]({row['bigramfreq']}@download)"
    trigramfreq = f"[trigram counts]({row['trigramfreq']}@download)"
    return f'{wordfreq}<br>{bigramfreq}<br>{trigramfreq}'


def _markdown_table(tsv_table):
    df = pd.read_csv(tsv_table, sep='\t')
    df['corpus word count'] = df['words'].apply(parse_big_number)
    df['vectors'] = df.apply(_vec_links, axis=1)
    df['ngram counts'] = df.apply(lambda x: '' if x['corpus'] == 'Wikipedia + OpenSubtitles' else _freq_links(x), axis=1)
    df['language'] = df.apply(lambda x: x['language'] if x['corpus'] == 'OpenSubtitles' else '', axis=1)
    df['lang'] = df.apply(lambda x: x['lang'] if x['corpus'] == 'OpenSubtitles' else '', axis=1)
    df = df[['language', 'lang', 'corpus', 'vectors', 'corpus word count', 'ngram counts']]
    return df.to_markdown(showindex=False)  # pandas usually uses index=False, but this is a kwarg that gets passed to tabulate


def _latex_table(tsv_table):
    df = pd.read_csv(tsv_table, sep='\t')
    df['word count'] = df['words'].apply(parse_big_number)
    df['mean words per line'] = df['mean_line_length']
    df = df.sort_values(['language', 'corpus'])
    df['language'] = df.apply(lambda x: x['language'] if x['corpus'] == 'OpenSubtitles' else '', axis=1)
    df = df[['language', 'corpus', 'word count', 'mean words per line']]
    return df.to_latex(index=False)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('table_type', choices=['latex', 'markdown'], help='select markdown or latex format')
    args = argparser.parse_args()

    if args.table_type == 'markdown':
        print(_markdown_table(os.path.join(path, 'paper_results', 'table_data.tsv')))
    elif args.table_type == 'latex':
        print(_latex_table(os.path.join(path, 'paper_results', 'table_data.tsv')))
