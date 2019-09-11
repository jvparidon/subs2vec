# subs2vec
subs2vec contains a number of Python 3.7 scripts and command line tools to evaluate a set of word vectors on semantic similarity, semantic and syntactic analogy, and lexical norm prediction tasks. In addition, the `subs2vec.py` script will take an OpenSubtitles archive or Wikipedia and go through all the steps to train a fastText model and produce word vectors as used in Van Paridon & Thompson (2019).  

Psycholinguists may be especially interested `norms.py` script, which evaluates the lexical norm prediction performance of a set of word vectors, but can also be used to predict lexical norms for unnormed words. For a more detailed explanation see the __how to use__ section.  

The scripts in this repository require [Python 3.7](https://www.python.org/downloads/) and some additional libraries that are easily installed through pip. (If you want to use the `subs2vec.py` script to train your own word embeddings, you will also need compiled fastText and word2vec binaries.)  

Pretrained models and word vectors are forthcoming.  
If you use subs2vec and/or pretrained models, please cite the arXiv paper (also forthcoming).  

## Contents of this repository
- `evaluation/`: Contains two subdirectories datasets and results of the evaluation of word vectors.
  - `datasets/`: Contains the evaluation datasets.
  - `results/`: Contains evaluation results and figures as used in Van Paridon & Thompson (2019)
- `analogies.py`: Evaluates semantic and syntactic analogy solving on all datasets for a set of word vectors in a given language. Can be used as a command line tool.
- `clean_subs.py`: Cleans and joins a subtitle corpus so that word embeddings can be trained on it. Can be used as a command line tool.
- `clean_wiki.py`: Cleans a Wikipedia corpus so that word embeddings can be trained on it. Can be used as a command line tool.
- `count_words.py`: Counts words in a corpus. Can be used as a command line tool.
- `deduplicate.py`: Removes duplicate lines from a corpus. Can be used as a command line tool.
- `eval_lang.py`: Evaluates all metrics (analogies, similarities, and norms) for a set of word vectors in a given language. Can be used as a command line tool.
- `frequencies.py`: Extracts word frequencies (and bigram and trigram frequencies) from a corpus. Can be used as a command line tool.
- `norms.py`: Evaluates lexical norm prediction on all datasets for a set of word vectors in a given language. Can be used as a command line tool.
- `plots.py`: Draws the plots included in Van Paridon & Thompson (2019).
- `shuffle_text.py`: Shuffles lines in a corpus. Can be used as a command line tool.
- `similarities.py`: Evaluates semantic similarity correlations on all datasets for a set of word vectors in a given language. Can be used as a command line tool.
- `subs2vec.py`: Creates word embeddings from a subtitle or Wikipedia corpus. Can be used as a command line tool. (Requires fastText and word2phrase binaries.)
- `utensils.py`: Contains some convenience functions, used for timing and logging.
- `vecs.py`: Contains methods for reading and writing word vectors, including reading into Python dicts, pandas DataFrames, and NumPy arrays.

## How to use
### Evaluating word embeddings
To evaluate word embeddings on analogies, semantic similarity, or lexical norm prediction as in Van Paridon & Thompson (2019), use:  
`python3 -m subs2vec.analogies [fr] [french_word_vectors.vec]`  
`python3 -m subs2vec.similarities [fr] [french_word_vectors.vec]`  
`python3 -m subs2vec.norms [fr] [french_word_vectors.vec]`  
subs2vec uses the two-letter ISO language codes, so French in the example is `fr`, English would be `en`, German would be `de`, etc.

### Extending lexical norms
`python3 -m subs2vec.norms [fr] [french_word_vectors.vec] --extend --norms=[french_norms_file.txt]`

### Extracting word frequencies
`python3 -m subs2vec.frequencies words`  
When looking up frequencies for specific words, bigrams, or trigrams, you may find that you cannot open the frequencies file (it can be very large). To retrieve items of interest use:   
`python3 -m subs2vec.lookup [frequencies_file.tsv] [list_of_items.txt]`  
Your list of items should be a simple text file, with each item you want to look up on its own line.
This method works for looking up word vectors in .vec files and lexical norms in .tsv files as well as for looking up frequencies.

### Training models
If you want to reproduce models as used in Van Paridon & Thompson (2019), you can use the `train_model` module.
To train a subtitle model in for example French, use:  
`python3 -m subs2vec.train_model [fr] subs --download --clean`  
For more detailed training options:  
`python3 -m subs2vec.train_model --help`

## API
For more detailed documentation of the package modules and API, see [subs2vec.readthedocs.io](https://subs2vec.readthedocs.io)

## Pretrained embeddings and word/bigram/trigram frequencies
Van Paridon & Thompson (2019) introduces pretrained embeddings and precomputed word/bigram/trigram frequencies in 50 languages.  
The files can be downloaded from [language archive]. Word vectors trained on subtitles are available, as well as vectors trained on Wikipedia, and a combination of subtitles and Wikipedia (for best performance).
