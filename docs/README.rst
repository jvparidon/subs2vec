=======
sub2vec
=======
sub2vec contains a number of Python 3.7 scripts and command line tools to evaluate a set of word vectors on semantic similarity, semantic and syntactic analogy, and lexical norm prediction tasks. In addition, the `sub2vec.py` script will take an OpenSubtitles archive or Wikipedia and go through all the steps to train a fastText model and produce word vectors as used in Van Paridon & Thompson (2019).

Psycholinguists may be especially interested `norms.py` script, which evaluates the lexical norm prediction performance of a set of word vectors, but can also be used to predict lexical norms for unnormed words. For a more detailed explanation see the **how to use** section.

The scripts in this repository require `Python 3.7 <https://www.python.org/downloads/>`_ and some additional libraries that are easily installed through pip. (If you want to use the `sub2vec.py` script to train your own word embeddings, you will also need compiled fastText and word2vec binaries.)  

Pretrained models and word vectors are forthcoming.  
If you use sub2vec and/or pretrained models, please cite the arXiv paper (also forthcoming).  

Contents of this repository
===========================
- ``evaluation/``: Contains two subdirectories datasets and results of the evaluation of word vectors.

  - ``datasets/``: Contains the evaluation datasets.
  - ``results/``: Contains evaluation results and figures as used in Van Paridon & Thompson (2019)

- ``analogies.py``: Evaluates semantic and syntactic analogy solving on all datasets for a set of word vectors in a given language. Can be used as a command line tool.
- ``clean_subs.py``: Cleans and joins a subtitle corpus so that word embeddings can be trained on it. Can be used as a command line tool.
- ``clean_wiki.py``: Cleans a Wikipedia corpus so that word embeddings can be trained on it. Can be used as a command line tool.
- ``count_words.py``: Counts words in a corpus. Can be used as a command line tool.
- ``deduplicate.py``: Removes duplicate lines from a corpus. Can be used as a command line tool.
- ``eval_lang.py``: Evaluates all metrics (analogies, similarities, and norms) for a set of word vectors in a given language. Can be used as a command line tool.
- ``frequencies.py``: Extracts word frequencies (and bigram and trigram frequencies) from a corpus. Can be used as a command line tool.
- ``norms.py``: Evaluates lexical norm prediction on all datasets for a set of word vectors in a given language. Can be used as a command line tool.
- ``plots.py``: Draws the plots included in Van Paridon & Thompson (2019).
- ``shuffle_text.py``: Shuffles lines in a corpus. Can be used as a command line tool.
- `similarities.py`: Evaluates semantic similarity correlations on all datasets for a set of word vectors in a given language. Can be used as a command line tool.
- ``sub2vec.py``: Creates word embeddings from a subtitle or Wikipedia corpus. Can be used as a command line tool. (Requires fastText and word2phrase binaries.)
- ``utensils.py``: Contains some convenience functions, used for timing and logging.
- ``vecs.py``: Contains methods for reading and writing word vectors, including reading into Python dicts, pandas DataFrames, and NumPy arrays.

How to use
==========
| To evaluate word vectors on a set of language-specific benchmarks:
| ``python3 vecs.py --filename=my_spanish_vectors.vec --lang=es`` (sub2vec uses the two-letter ISO 639-1 language codes)  

| For more detailed evaluation options:
| ``python3 vecs.py --help``

| To train a sub2vec model:
| ``python3 sub2vec.py --subs_dir=../OpenSubtitles2018 --lang=es``

| For more detailed training options:
| ``python3 sub2vec.py --help``

