"""Download datasets for training subs2vec models (not Windows-compatible)."""
import subprocess
import pandas as pd
import argparse
import os
path = os.path.dirname(__file__)


def download_corpus(lang, source):
    """Convenient method for downloading corpora.

    Uses the subprocess module and curl to download corpora.
    Not Windows-compatible.

    :param lang: language to download (use 2-letter ISO code)
    :param source: corpus to download, (options are "subs" or "wiki")
    """
    urls = {
        'subs': f'http://opus.nlpl.eu/download.php?f=OpenSubtitles/v2018/raw/{lang}.zip',
        'wiki': f'http://dumps.wikimedia.your.org/{lang}wiki/latest/{lang}wiki-latest-pages-meta-current.xml.bz2'
    }
    subprocess.run(['curl', '-OLk', urls[source]])


def download_vecs(lang, source, binaries=False):
    """Convenient method for downloading vectors.

    Uses the subprocess module and curl to download corpora.
    Not Windows-compatible.

    :param lang: language to download (use 2-letter ISO code)
    :param source: corpus to download, (options are "subs", "wiki", or "wiki+subs")
    :param binaries: download binaries instead of vecs, boolean (set to False by default)
    """
    df = pd.read_csv(os.path.join(path, 'paper_results', 'corpus_data.tsv'), sep='\t')
    if binaries:
        filetype = 'binary'  # look up model binary url in df
    else:
        filetype = 'topvecs'  # look up url for top 1M vecs in df
    url = df.loc[(df['lang'] == lang) & (df['vecs'] == source), filetype].values[0]
    fname = f'{source.replace("+", "-")}.{lang}.1e6.zip'
    subprocess.run(['curl', '-Lo', fname, f'{url}@download'])


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='download datasets for training subs2vec models (not Windows-compatible)')
    argparser.add_argument('lang', help='language to download (use 2-letter ISO code)')
    argparser.add_argument('source', choices=['subs', 'wiki', 'wiki+subs'], help='what source to download from')
    argparser.add_argument('--vecs', action='store_true', help='download vectors')
    argparser.add_argument('--binaries', action='store_true', help='download binaries')
    argparser.add_argument('--corpus', action='store_true', help='download corpus')
    args = argparser.parse_args()

    if args.vecs:
        download_vecs(args.lang, args.source)
    if args.binaries:
        download_vecs(args.lang, args.source, binaries=args.binaries)
    if args.corpus:
        download_corpus(args.lang, args.source)
