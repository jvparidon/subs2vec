# subs2vec
Van Paridon & Thompson (2019) introduces pretrained embeddings and precomputed word/bigram/trigram frequencies in 50 languages. The files can be downloaded from [language archive]. Word vectors trained on subtitles are available, as well as vectors trained on Wikipedia, and a combination of subtitles and Wikipedia (for best performance).

This repository contains the subs2vec module, a number of Python 3.7 scripts and command line tools to evaluate a set of word vectors on semantic similarity, semantic and syntactic analogy, and lexical norm prediction tasks. In addition, the `subs2vec.py` script will take an OpenSubtitles archive or Wikipedia and go through all the steps to train a fastText model and produce word vectors as used in Van Paridon & Thompson (2019).  

Psycholinguists may be especially interested `norms` script, which evaluates the lexical norm prediction performance of a set of word vectors, but can also be used to predict lexical norms for un-normed words. For a more detailed explanation see the __How to use -> Extending lexical norms__ section.  

The scripts in this repository require [Python 3.7](https://www.python.org/downloads/) and some additional libraries that are easily installed through pip. (If you want to use the `subs2vec.py` script to train your own word embeddings, you will also need compiled fastText and word2vec binaries.)  

If you use any of the subs2vec code and/or pretrained models, please cite the arXiv paper (Van Paridon & Thompson, 2019, forthcoming).  

## How to use
In general, the submodules of subs2vec can be run as Python modules using the -m flag:  
`python3 -m subs2vec.submodule_name`  
Normally, this only works if you are in the subs2vec directory. If you want to be able to use the subs2vec commands anywhere, consider installing 
the subs2vec package using:  
`python3 setup.py install`  
This will not make any major changes to your system, it just copies the subs2vec package to a place where the Python interpreter knows to 
look for it.

### Evaluating word embeddings
To evaluate word embeddings on analogies, semantic similarity, or lexical norm prediction as in Van Paridon & Thompson (2019), use:  
`python3 -m subs2vec.analogies fr french_word_vectors.vec`  
`python3 -m subs2vec.similarities fr french_word_vectors.vec`  
`python3 -m subs2vec.norms fr french_word_vectors.vec`  
subs2vec uses the two-letter ISO language codes, so French in the example is `fr`, English would be `en`, German would be `de`, etc.

All datasets used for evaluation, including the lexical norms, are stored in `subs2vec/evaluation/datasets/`.  
Results from Van Paridon & Thompson (2019) are in `subs2vec/evaluation/article_results/`.

### Extending lexical norms
To extend lexical norms (either norms you have collected yourself, or norms provided in this repository) use:  
`python3 -m subs2vec.norms fr french_word_vectors.vec --extend_norms=french_norms_file.txt`  
The norms file should be a tab-separated text file, with the first line containing column names and the column containing the words should be called `word`. Unobserved cells should be left empty. If you are unsure how to generate this file, you can create your list in Excel and then use `Save as... tab-delimited text`.

### Extracting word frequencies
The subtitle corpus used in Van Paridon & Thompson (2019) was also used to compile the word frequencies in SUBTLEX [ref]. That same corpus can be used to compile bigram and trigram frequencies as well.
To extract word, bigram, or trigram frequencies from a text file yourself, `fr.txt` for instance, use:  
`python3 -m subs2vec.frequencies fr.txt`  

In general, however, we recommend downloading the precompiled frequencies files from [language archive] and looking frequencies up in those.  
When looking up frequencies for specific words, bigrams, or trigrams, you may find that you cannot open the frequencies files (they can be very large). To retrieve items of interest use:   
`python3 -m subs2vec.lookup frequencies_file.tsv list_of_items.txt`  
Your list of items should be a simple text file, with each item you want to look up on its own line.
This lookup scripts works for looking up frequencies, but it works for looking up word vectors in .vec files and lexical norms in .tsv files as well.

### Removing duplicate lines
subs2vec comes with a script that removes duplicate lines from text files. We used it to remove duplicate lines from training corpora, but it works for any text file.  
To remove duplicates from `fr.txt` for example, use:  
`python3 -m subs2vec.deduplicate fr.txt`

### Training models
If you want to reproduce models as used in Van Paridon & Thompson (2019), you can use the `train_model` module.
For instance, the steps to create a subtitle corpus are:
1. Download a corpus:  
`python3 -m subs2vec.download fr subs`  
2. Clean the corpus:  
`python3 -m subs2vec.clean_subs fr.zip --strip --join`  
3. Deduplicate the lines in the corpus:  
`python3 -m subs2vec.deduplicate fr.txt`  
4. Train a fastText model on the subtitle corpus:  
`python3 -m subs2vec.train_model fr subs dedup.fr.txt`  

For more detailed training options:  
`python3 -m subs2vec.train_model --help`

## API
For more detailed documentation of the package modules and API, see [subs2vec.readthedocs.io](https://subs2vec.readthedocs.io)
