"""Train a model using the default parameters from Van Paridon & Thompson (2019).

Use of this module requires working binaries for fastText and word2vec on the path and plenty of RAM.
Please note that even on a very fast desktop, training could take hours or days.
"""
import argparse
import subprocess as sp
from .utensils import log_timer
import psutil
import logging
logging.basicConfig(format='[{levelname}] {message}', style='{', level=logging.INFO)
cpu_count = psutil.cpu_count(logical=False)  # logical=False to count only physical cores


@log_timer
def train_fasttext(training_data, prefix, lang, d=300, neg=10, epoch=10, t=.0001):
    """Train a fastText model on a given training corpus.

    Requires a working fastText binary on the path.

    :param training_data: text file containing the training corpus
    :param prefix: prefix to use for the model binary and vector filenames
    :param lang: language tag to use for the model binary and vector filenames
    :param d: number of dimensions in the vector (default is 300)
    :param neg: number of negative samples (fastText default is 5, subs2vec default used here is 10)
    :param epoch: number of training epochs (fastText default is 5, subs2vec default used here is 10)
    :param t: sampling threshold (default is .0001)
    :return: tuple of filenames for model binary and vectors
    """
    model_name = f'{prefix}.{lang}'
    binary = ['fasttext']
    method = ['skipgram']
    train = ['-input', training_data]
    output = ['-output', model_name]
    neg = ['-neg', str(neg)]
    epoch = ['-epoch', str(epoch)]
    t = ['-t', str(t)]
    d = ['-dim', str(d)]
    thread = ['-thread', str(cpu_count)]
    if logging.getLogger().isEnabledFor(logging.INFO):
        sp.run(binary + method + train + output + neg + epoch + t + d + thread)
    else:
        sp.run(binary + method + train + output + neg + epoch + t + d + thread, stdout=sp.DEVNULL)
    model = f'{model_name}.bin'
    vecs = f'{model_name}.vec'
    return model, vecs


@log_timer
def build_phrases(training_data, phrase_pass=5):
    """Use word2phrase to connect common phrases.

    Uses the word2phrase tool to connect high mutual information phrases such as "New York" using underscores, so fastText will treat them as a single lexical item.
    Requires a working word2phrase (included in word2vec) binary on the path.

    :param training_data: text file containing the training corpus
    :param phrase_pass: number of passes to do over the training file (default is 5)
    :return: filename of the phrase-joined corpus
    """
    base_fname = training_data.replace('.txt', '')
    for i in range(phrase_pass):
        t = (2 ** (phrase_pass - i - 1)) * 100
        out_fname = f'{base_fname}.{i + 1}pass.d5.t{t}.txt'
        binary = ['word2phrase']
        train = ['-train', training_data]
        output = ['-output', out_fname]
        d = ['-min-count', str(5)]
        t = ['-threshold', str(t)]
        if logging.getLogger().isEnabledFor(logging.INFO):
            sp.run(binary + train + output + d + t)
        else:
            sp.run(binary + train + output + d + t, stdout=sp.DEVNULL)
        training_data = out_fname
    return out_fname


def fix_encoding(training_data):
    """Fix utf-8 file encoding after word2phrase mangles it (happens sometimes).

    :param training_data: file containing text with encoding that needs fixing
    :return: filename of repaired text file
    """
    out_fname = training_data.replace('.txt', '.utf-8.txt')
    with open(training_data, 'r', encoding='utf-8', errors='ignore') as in_file, open(out_fname, 'w', encoding='utf-8') as out_file:
        for line in in_file:
            out_file.write(line)
    return out_fname


def lowercase(training_data):
    """Cast a text file to lower case.

    :param training_data: file containing text to cast to lower case
    :return: filename of lower cased text file
    """
    out_fname = training_data.replace('.txt', '.lower.txt')
    with open(training_data, 'r', encoding='utf-8') as in_file, open(out_fname, 'w', encoding='utf-8') as out_file:
        for line in in_file:
            out_file.write(line.lower())
    return out_fname


@log_timer
def generate(lang, prefix, training_data, lowercase=False):
    """Generate a fastText model using default parameters from Van Paridon & Thompson (2019).

    :param lang: language tag to use for the model binary and vector filenames
    :param training_data: text file containing the training corpus
    :param prefix: prefix to use for the model binary and vector filenames
    :param lowercase: boolean setting whether to cast training corpus to lower case (default is `False`)
    """
    if lowercase:
        logging.info(f'lowercasing {training_data}')
        training_data = lowercase(training_data)

    # build phrases
    logging.info('building phrases for {}'.format(training_data))
    training_data = build_phrases(training_data)

    # fix potential broken utf-8 encoding
    logging.info('checking (and fixing) utf-8 encoding for {}'.format(training_data))
    training_data = fix_encoding(training_data)

    # train fastText model
    logging.info('training fastText model on {}'.format(training_data))
    results = train_fasttext(training_data=training_data, lang=lang, prefix=prefix)
    model, vecs = results
    logging.info('model binary at {}'.format(model))
    logging.info('word vectors at {}'.format(vecs))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='generate a fastText model from OpenSubtitles and Wikipedia data')
    argparser.add_argument('lang',
                           help='source language (OpenSubtitles and Wikipedia data uses ISO 639-1 codes)')
    argparser.add_argument('prefix',
                           help='source data, use one of {wiki, sub, wiki-sub} if using automatic data preparation')
    argparser.add_argument('training_data',
                           help='filename of text file containing the training corpus')
    args = argparser.parse_args()

    generate(**vars(args))
