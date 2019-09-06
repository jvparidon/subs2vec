# sub2vec
Tools for training word2vec style models on a subtitle corpus

sub2vec.py is a Python3 command line tool that takes an OpenSubtitles archive and goes through all the steps to create a fastText model from the subtitle data.  
Requires utensilities, fastText and word2vec.  

Pretrained models are forthcoming, watch this space.  
If you use sub2vec and/or pretrained models, please cite the arXiv paper (also forthcoming).  
(And if you use OpenSubtitles data please credit the OpenSubtitles.org team.)

## Scripts included in this repository
- `analogies.py`: Evaluates semantic and syntactic analogy solving on all datasets for a set of word vectors in a given language. Can be used as a command line tool.
- `clean_subs.py`: ?
- `clean_wiki.py`: ?
- `count_words.py`: Counts words in a corpus. Can be used as a command line tool.
- `deduplicate.py`: Removes duplicate lines from a corpus. Can be used as a command line tool.
- `eval_lang.py`: Evaluates all metrics (analogies, similarities, and norms) for a set of word vectors in a given language. Can be used as a command line tool.
- `frequencies.py`: Extracts word frequencies (and bigram and trigram frequencies) from a corpus. Can be used as a command line tool.
- `norms.py`: Evaluates lexical norm prediction on all datasets for a set of word vectors in a given language. Can be used as a command line tool.
- `plots.py`: Draws the plots included in Van Paridon & Thompson (2019).
- `shuffle_text.py`: Shuffles lines in a corpus. Can be used as a command line tool.
- `similarities.py`: Evaluates semantic similarity correlations on all datasets for a set of word vectors in a given language. Can be used as a command line tool.
- `sub2vec.py`: Creates word embeddings from a subtitle or Wikipedia corpus. Can be used as a command line tool. (Requires fastText and word2phrase binaries.)
- `utensils.py`: Contains some convenience functions, used for timing and logging.
- `vecs.py`: Contains methods for reading and writing word vectors, including reading into Python dicts, pandas DataFrames, and NumPy arrays.

## How to use
To evaluate word vectors on a set of language-specific benchmarks:  
`python3 vecs.py --filename=my_spanish_vectors.vec --lang=es` (sub2vec uses the ISO 639-1 language codes)  
For more detailed evaluation options:  
`python3 vecs.py --help`

To train a sub2vec model:  
`python3 sub2vec.py --subs_dir=../OpenSubtitles2018 --lang=es`  
For more detailed training options:  
`python3 sub2vec.py --help`
