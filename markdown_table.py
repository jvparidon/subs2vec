import pandas as pd


def parse_big_number(num):
    if num < 1e3:
        num = f'{num}'
    elif num < 1e6:
        num = f'{num / 1e3:.0f}K'
    elif num < 1e9:
        num = f'{num / 1e6:.0f}M'
    else:
        num = f'{num / 1e9:.0f}B'
    return num


def vec_links(row):
    topvecs = f"[top 1M vectors]({row['topvecs']}@download)"
    allvecs = f"[all vectors]({row['allvecs']}@download)"
    binary = f"[model binary]({row['binary']}@download)"
    return f'{topvecs}<br>{allvecs}<br>{binary}'


def freq_links(row):
    wordfreq = f"[word counts]({row['wordfreq']}@download)"
    bigramfreq = f"[bigram counts]({row['bigramfreq']}@download)"
    trigramfreq = f"[trigram counts]({row['trigramfreq']}@download)"
    return f'{wordfreq}<br>{bigramfreq}<br>{trigramfreq}'


def markdown_table(tsv_table):
    df = pd.read_csv(tsv_table, sep='\t')
    df['corpus word count'] = df['wordcount'].apply(parse_big_number)
    df['vectors'] = df.apply(vec_links, axis=1)
    df['ngram counts'] = df.apply(lambda x: '' if x['corpus'] == 'Wikipedia + OpenSubtitles' else freq_links(x), axis=1)
    df['language'] = df.apply(lambda x: x['language'] if x['corpus'] == 'OpenSubtitles' else '', axis=1)
    df['lang'] = df.apply(lambda x: x['lang'] if x['corpus'] == 'OpenSubtitles' else '', axis=1)
    df = df[['language', 'lang', 'corpus', 'vectors', 'corpus word count', 'ngram counts']]
    return df.to_markdown(showindex=False)  # pandas usually uses index=False, but this is a kwarg that gets passed to tabulate


if __name__ == '__main__':
    print(markdown_table('subs2vec/paper_results/corpus_data.tsv'))
