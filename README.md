# subs2vec
Van Paridon & Thompson (2019) introduces pretrained embeddings and precomputed word/bigram/trigram frequencies in 55 languages. The files can be downloaded from [language archive]. Word vectors trained on subtitles are available, as well as vectors trained on Wikipedia, and a combination of subtitles and Wikipedia (for best performance).

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
Any missing dependencies can be installed using:  
`pip3 install -r requirements.txt`

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
For an overview of norms that come included in the repo (and their authors), see [this list](https://github.com/jvparidon/subs2vec/blob/master/subs2vec/datasets/norms_table.tsv). For the norms datasets themselves, look inside [this directory](https://github.com/jvparidon/subs2vec/tree/master/subs2vec/datasets/norms).

### Extracting word frequencies
The subtitle corpus used in Van Paridon & Thompson (2019) was also used to compile the word frequencies in SUBTLEX [ref]. That same corpus can be used to compile bigram and trigram frequencies as well.
To extract word, bigram, or trigram frequencies from a text file yourself, `fr.txt` for instance, use:  
`python3 -m subs2vec.frequencies fr.txt`  

In general, however, we recommend downloading the precompiled frequencies files from [language archive] and looking frequencies up in those.  
When looking up frequencies for specific words, bigrams, or trigrams, you may find that you cannot open the frequencies files (they can be very large). To retrieve items of interest use:   
`python3 -m subs2vec.lookup frequencies_file.tsv list_of_items.txt`  
Your list of items should be a simple text file, with each item you want to look up on its own line.
This lookup scripts works for looking up frequencies, but it finds lines in any plain text file, so it works for looking up word vectors in .vec files as well.

### Removing duplicate lines
subs2vec comes with a module that removes duplicate lines from text files. We used it to remove duplicate lines from training corpora, but it works for any text file.  
To remove duplicates from `fr.txt` for example, use:  
`python3 -m subs2vec.deduplicate fr.txt`

### Training models
If you want to reproduce models as used in Van Paridon & Thompson (2019), you can use the `train_model` module.
For instance, the steps to create a subtitle corpus are:
1. Download a corpus:  
`python3 -m subs2vec.download fr subs`  
2. Clean the corpus:  
`python3 -m subs2vec.clean_subs fr --strip --join`  
3. Deduplicate the lines in the corpus:  
`python3 -m subs2vec.deduplicate fr.txt`  
4. Train a fastText model on the subtitle corpus:  
`python3 -m subs2vec.train_model fr subs dedup.fr.txt`  
This last step requires the binaries for [fastText](https://github.com/facebookresearch/fastText) and [word2phrase (part of word2vec)](https://github.com/tmikolov/word2vec) to be downloaded, built, and discoverable on your system.

For more detailed training options:  
`python3 -m subs2vec.train_model --help`

## API
For more detailed documentation of the package modules and API, see [subs2vec.readthedocs.io](https://subs2vec.readthedocs.io)

## Downloading datasets
This table contains links to the top 1 million word vectors in each language, as well all vectors, model binaries, and the word, bigram, and trigram frequencies in the subtitle and Wikipedia corpora.

| language | lang | corpus | vectors | corpus word count | ngram frequencies |
|---|---|---|---|---:|---|
| Afrikaans | af | OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_59a61205_dfc3_4eec_9fd9_311b3f65c9a5/datastream/OBJ/download) / [all](https://archive.mpi.nl/islandora/object/lat%3A1839_486caf84_5d28_439c_a09f_6b90b7fe79dd/datastream/OBJ/download) / [binary](https://archive.mpi.nl/islandora/object/lat%3A1839_8d87878f_ce0b_4221_81b3_5fff04eec335/datastream/OBJ/download) |    323K | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_a1a82d13_be9d_4024_bbfe_90de100fcd3c/datastream/OBJ/download) / [bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_1f671cfa_131d_4fa8_bfe2_021a59952256/datastream/OBJ/download) / [trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_e4a8e2f0_2cfa_4d5a_8d22_864ef02d7f26/datastream/OBJ/download) |
| | | Wikipedia | [top 1M]() / [all]() / [binary]() |     17M | [unigrams]() / [bigrams]() / [trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]() / [all]() / [binary]() | | |
| Arabic | ar | OpenSubtitles | [top 1M]() / [all]() / [binary]() |    188M | [unigrams]() / [bigrams]() / [trigrams]() |
| | | Wikipedia | wiki.ar.1M.vec |    119M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ar.1M.vec | | |
| Bulgarian | bg | OpenSubtitles | subs.bg.1M.vec |    246M | dedup.bg.words.unigrams.tsv dedup.bg.words.bigrams.tsv dedup.bg.words.trigrams.tsv |
| | | Wikipedia | wiki.bg.1M.vec |     53M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.bg.1M.vec | | |
| Bengali | bn | OpenSubtitles | subs.bn.1M.vec |   2227K | dedup.bn.words.unigrams.tsv dedup.bn.words.bigrams.tsv dedup.bn.words.trigrams.tsv |
| | | Wikipedia | wiki.bn.1M.vec |     18M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.bn.1M.vec | | |
| Breton | br | OpenSubtitles | subs.br.1M.vec |    110K | dedup.br.words.unigrams.tsv dedup.br.words.bigrams.tsv dedup.br.words.trigrams.tsv |
| | | Wikipedia | wiki.br.1M.vec |   7644K | |
| | | Wikipedia + OpenSubtitles | wiki-subs.br.1M.vec | | |
| Bosnian | bs | OpenSubtitles | subs.bs.1M.vec |     91M | dedup.bs.words.unigrams.tsv dedup.bs.words.bigrams.tsv dedup.bs.words.trigrams.tsv |
| | | Wikipedia | wiki.bs.1M.vec |     13M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.bs.1M.vec | | |
| Catalan | ca | OpenSubtitles | subs.ca.1M.vec |   3098K | dedup.ca.words.unigrams.tsv dedup.ca.words.bigrams.tsv dedup.ca.words.trigrams.tsv |
| | | Wikipedia | wiki.ca.1M.vec |    175M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ca.1M.vec | | |
| Czech | cs | OpenSubtitles | subs.cs.1M.vec |    249M | dedup.cs.words.unigrams.tsv dedup.cs.words.bigrams.tsv dedup.cs.words.trigrams.tsv |
| | | Wikipedia | wiki.cs.1M.vec |    100M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.cs.1M.vec | | |
| Danish | da | OpenSubtitles | subs.da.1M.vec |     87M | dedup.da.words.unigrams.tsv dedup.da.words.bigrams.tsv dedup.da.words.trigrams.tsv |
| | | Wikipedia | wiki.da.1M.vec |     56M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.da.1M.vec | | |
| German | de | OpenSubtitles | subs.de.1M.vec |    139M | dedup.de.words.unigrams.tsv dedup.de.words.bigrams.tsv dedup.de.words.trigrams.tsv |
| | | Wikipedia | wiki.de.1M.vec |    976M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.de.1M.vec | | |
| Greek | el | OpenSubtitles | subs.el.1M.vec |    271M | dedup.el.words.unigrams.tsv dedup.el.words.bigrams.tsv dedup.el.words.trigrams.tsv |
| | | Wikipedia | wiki.el.1M.vec |     58M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.el.1M.vec | | |
| English | en | OpenSubtitles | subs.en.1M.vec |    750M | dedup.en.words.unigrams.tsv dedup.en.words.bigrams.tsv dedup.en.words.trigrams.tsv |
| | | Wikipedia | wiki.en.1M.vec |   2477M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.en.1M.vec | | |
| Esperanto | eo | OpenSubtitles | subs.eo.1M.vec |    381K | dedup.eo.words.unigrams.tsv dedup.eo.words.bigrams.tsv dedup.eo.words.trigrams.tsv |
| | | Wikipedia | wiki.eo.1M.vec |     37M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.eo.1M.vec | | |
| Spanish | es | OpenSubtitles | subs.es.1M.vec |    514M | dedup.es.words.unigrams.tsv dedup.es.words.bigrams.tsv dedup.es.words.trigrams.tsv |
| | | Wikipedia | wiki.es.1M.vec |    585M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.es.1M.vec | | |
| Estonian | et | OpenSubtitles | subs.et.1M.vec |     60M | dedup.et.words.unigrams.tsv dedup.et.words.bigrams.tsv dedup.et.words.trigrams.tsv |
| | | Wikipedia | wiki.et.1M.vec |     29M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.et.1M.vec | | |
| Basque | eu | OpenSubtitles | subs.eu.1M.vec |   3400K | dedup.eu.words.unigrams.tsv dedup.eu.words.bigrams.tsv dedup.eu.words.trigrams.tsv |
| | | Wikipedia | wiki.eu.1M.vec |     20M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.eu.1M.vec | | |
| Farsi | fa | OpenSubtitles | subs.fa.1M.vec |     45M | dedup.fa.words.unigrams.tsv dedup.fa.words.bigrams.tsv dedup.fa.words.trigrams.tsv |
| | | Wikipedia | wiki.fa.1M.vec |     86M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.fa.1M.vec | | |
| Finnish | fi | OpenSubtitles | subs.fi.1M.vec |    116M | dedup.fi.words.unigrams.tsv dedup.fi.words.bigrams.tsv dedup.fi.words.trigrams.tsv |
| | | Wikipedia | wiki.fi.1M.vec |     73M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.fi.1M.vec | | |
| French | fr | OpenSubtitles | subs.fr.1M.vec |    335M | dedup.fr.words.unigrams.tsv dedup.fr.words.bigrams.tsv dedup.fr.words.trigrams.tsv |
| | | Wikipedia | wiki.fr.1M.vec |    724M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.fr.1M.vec | | |
| Galician | gl | OpenSubtitles | subs.gl.1M.vec |   1666K | dedup.gl.words.unigrams.tsv dedup.gl.words.bigrams.tsv dedup.gl.words.trigrams.tsv |
| | | Wikipedia | wiki.gl.1M.vec |     40M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.gl.1M.vec | | |
| Hebrew | he | OpenSubtitles | subs.he.1M.vec |    169M | dedup.he.words.unigrams.tsv dedup.he.words.bigrams.tsv dedup.he.words.trigrams.tsv |
| | | Wikipedia | wiki.he.1M.vec |    132M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.he.1M.vec | | |
| Hindi | hi | OpenSubtitles | subs.hi.1M.vec |    659K | dedup.hi.words.unigrams.tsv dedup.hi.words.bigrams.tsv dedup.hi.words.trigrams.tsv |
| | | Wikipedia | wiki.hi.1M.vec |     31M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.hi.1M.vec | | |
| Croatian | hr | OpenSubtitles | subs.hr.1M.vec |    241M | dedup.hr.words.unigrams.tsv dedup.hr.words.bigrams.tsv dedup.hr.words.trigrams.tsv |
| | | Wikipedia | wiki.hr.1M.vec |     42M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.hr.1M.vec | | |
| Hungarian | hu | OpenSubtitles | subs.hu.1M.vec |    227M | dedup.hu.words.unigrams.tsv dedup.hu.words.bigrams.tsv dedup.hu.words.trigrams.tsv |
| | | Wikipedia | wiki.hu.1M.vec |    120M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.hu.1M.vec | | |
| Armenian | hy | OpenSubtitles | subs.hy.1M.vec |     23K | dedup.hy.words.unigrams.tsv dedup.hy.words.bigrams.tsv dedup.hy.words.trigrams.tsv |
| | | Wikipedia | wiki.hy.1M.vec |     38M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.hy.1M.vec | | |
| Indonesian | id | OpenSubtitles | subs.id.1M.vec |     65M | dedup.id.words.unigrams.tsv dedup.id.words.bigrams.tsv dedup.id.words.trigrams.tsv |
| | | Wikipedia | wiki.id.1M.vec |     69M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.id.1M.vec | | |
| Icelandic | is | OpenSubtitles | subs.is.1M.vec |   7474K | dedup.is.words.unigrams.tsv dedup.is.words.bigrams.tsv dedup.is.words.trigrams.tsv |
| | | Wikipedia | wiki.is.1M.vec |   7196K | |
| | | Wikipedia + OpenSubtitles | wiki-subs.is.1M.vec | | |
| Italian | it | OpenSubtitles | subs.it.1M.vec |    277M | dedup.it.words.unigrams.tsv dedup.it.words.bigrams.tsv dedup.it.words.trigrams.tsv |
| | | Wikipedia | wiki.it.1M.vec |    476M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.it.1M.vec | | |
| Japanese | ja | OpenSubtitles | subs.ja.1M.vec |   3027K | dedup.ja.words.unigrams.tsv dedup.ja.words.bigrams.tsv dedup.ja.words.trigrams.tsv |
| | | Wikipedia | wiki.ja.1M.vec |     23M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ja.1M.vec | | |
| Georgian | ka | OpenSubtitles | subs.ka.1M.vec |   1108K | dedup.ka.words.unigrams.tsv dedup.ka.words.bigrams.tsv dedup.ka.words.trigrams.tsv |
| | | Wikipedia | wiki.ka.1M.vec |     15M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ka.1M.vec | | |
| Kazakh | kk | OpenSubtitles | subs.kk.1M.vec |     13K | dedup.kk.words.unigrams.tsv dedup.kk.words.bigrams.tsv dedup.kk.words.trigrams.tsv |
| | | Wikipedia | wiki.kk.1M.vec |     18M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.kk.1M.vec | | |
| Korean | ko | OpenSubtitles | subs.ko.1M.vec |   6834K | dedup.ko.words.unigrams.tsv dedup.ko.words.bigrams.tsv dedup.ko.words.trigrams.tsv |
| | | Wikipedia | wiki.ko.1M.vec |     62M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ko.1M.vec | | |
| Lithuanian | lt | OpenSubtitles | subs.lt.1M.vec |   6252K | dedup.lt.words.unigrams.tsv dedup.lt.words.bigrams.tsv dedup.lt.words.trigrams.tsv |
| | | Wikipedia | wiki.lt.1M.vec |     23M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.lt.1M.vec | | |
| Latvian | lv | OpenSubtitles | subs.lv.1M.vec |   2167K | dedup.lv.words.unigrams.tsv dedup.lv.words.bigrams.tsv dedup.lv.words.trigrams.tsv |
| | | Wikipedia | wiki.lv.1M.vec |     13M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.lv.1M.vec | | |
| Macedonian | mk | OpenSubtitles | subs.mk.1M.vec |     20M | dedup.mk.words.unigrams.tsv dedup.mk.words.bigrams.tsv dedup.mk.words.trigrams.tsv |
| | | Wikipedia | wiki.mk.1M.vec |     26M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.mk.1M.vec | | |
| Malayalam | ml | OpenSubtitles | subs.ml.1M.vec |   1520K | dedup.ml.words.unigrams.tsv dedup.ml.words.bigrams.tsv dedup.ml.words.trigrams.tsv |
| | | Wikipedia | wiki.ml.1M.vec |     10M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ml.1M.vec | | |
| Malay | ms | OpenSubtitles | subs.ms.1M.vec |     12M | dedup.ms.words.unigrams.tsv dedup.ms.words.bigrams.tsv dedup.ms.words.trigrams.tsv |
| | | Wikipedia | wiki.ms.1M.vec |     28M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ms.1M.vec | | |
| Dutch | nl | OpenSubtitles | subs.nl.1M.vec |    264M | dedup.nl.words.unigrams.tsv dedup.nl.words.bigrams.tsv dedup.nl.words.trigrams.tsv |
| | | Wikipedia | wiki.nl.1M.vec |    248M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.nl.1M.vec | | |
| Norwegian | no | OpenSubtitles | subs.no.1M.vec |     45M | dedup.no.words.unigrams.tsv dedup.no.words.bigrams.tsv dedup.no.words.trigrams.tsv |
| | | Wikipedia | wiki.no.1M.vec |     90M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.no.1M.vec | | |
| Poland | pl | OpenSubtitles | subs.pl.1M.vec |    250M | dedup.pl.words.unigrams.tsv dedup.pl.words.bigrams.tsv dedup.pl.words.trigrams.tsv |
| | | Wikipedia | wiki.pl.1M.vec |    232M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.pl.1M.vec | | |
| Portuguese | pt | OpenSubtitles | subs.pt.1M.vec |    257M | dedup.pt.words.unigrams.tsv dedup.pt.words.bigrams.tsv dedup.pt.words.trigrams.tsv |
| | | Wikipedia | wiki.pt.1M.vec |    238M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.pt.1M.vec | | |
| Romanian | ro | OpenSubtitles | subs.ro.1M.vec |    434M | dedup.ro.words.unigrams.tsv dedup.ro.words.bigrams.tsv dedup.ro.words.trigrams.tsv |
| | | Wikipedia | wiki.ro.1M.vec |     65M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ro.1M.vec | | |
| Russian | ru | OpenSubtitles | subs.ru.1M.vec |    152M | dedup.ru.words.unigrams.tsv dedup.ru.words.bigrams.tsv dedup.ru.words.trigrams.tsv |
| | | Wikipedia | wiki.ru.1M.vec |    390M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ru.1M.vec | | |
| Sinhalese | si | OpenSubtitles | subs.si.1M.vec |   3493K | dedup.si.words.unigrams.tsv dedup.si.words.bigrams.tsv dedup.si.words.trigrams.tsv |
| | | Wikipedia | wiki.si.1M.vec |   5980K | |
| | | Wikipedia + OpenSubtitles | wiki-subs.si.1M.vec | | |
| Slovak | sk | OpenSubtitles | subs.sk.1M.vec |     47M | dedup.sk.words.unigrams.tsv dedup.sk.words.bigrams.tsv dedup.sk.words.trigrams.tsv |
| | | Wikipedia | wiki.sk.1M.vec |     28M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.sk.1M.vec | | |
| Slovene | sl | OpenSubtitles | subs.sl.1M.vec |    106M | dedup.sl.words.unigrams.tsv dedup.sl.words.bigrams.tsv dedup.sl.words.trigrams.tsv |
| | | Wikipedia | wiki.sl.1M.vec |     31M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.sl.1M.vec | | |
| Albanian | sq | OpenSubtitles | subs.sq.1M.vec |     11M | dedup.sq.words.unigrams.tsv dedup.sq.words.bigrams.tsv dedup.sq.words.trigrams.tsv |
| | | Wikipedia | wiki.sq.1M.vec |     17M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.sq.1M.vec | | |
| Serbian | sr | OpenSubtitles | subs.sr.1M.vec |    343M | dedup.sr.words.unigrams.tsv dedup.sr.words.bigrams.tsv dedup.sr.words.trigrams.tsv |
| | | Wikipedia | wiki.sr.1M.vec |     69M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.sr.1M.vec | | |
| Swedish | sv | OpenSubtitles | subs.sv.1M.vec |    101M | dedup.sv.words.unigrams.tsv dedup.sv.words.bigrams.tsv dedup.sv.words.trigrams.tsv |
| | | Wikipedia | wiki.sv.1M.vec |    143M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.sv.1M.vec | | |
| Tamil | ta | OpenSubtitles | subs.ta.1M.vec |    123K | dedup.ta.words.unigrams.tsv dedup.ta.words.bigrams.tsv dedup.ta.words.trigrams.tsv |
| | | Wikipedia | wiki.ta.1M.vec |     17M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ta.1M.vec | | |
| Telugu | te | OpenSubtitles | subs.te.1M.vec |    103K | dedup.te.words.unigrams.tsv dedup.te.words.bigrams.tsv dedup.te.words.trigrams.tsv |
| | | Wikipedia | wiki.te.1M.vec |     15M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.te.1M.vec | | |
| Thai | th | OpenSubtitles | subs.th.1M.vec |     10M | dedup.th.words.unigrams.tsv dedup.th.words.bigrams.tsv dedup.th.words.trigrams.tsv |
| | | Wikipedia | wiki.th.1M.vec |     12M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.th.1M.vec | | |
| Tagalog | tl | OpenSubtitles | subs.tl.1M.vec |     87K | dedup.tl.words.unigrams.tsv dedup.tl.words.bigrams.tsv dedup.tl.words.trigrams.tsv |
| | | Wikipedia | wiki.tl.1M.vec |   6515K | |
| | | Wikipedia + OpenSubtitles | wiki-subs.tl.1M.vec | | |
| Turkish | tr | OpenSubtitles | subs.tr.1M.vec |    239M | dedup.tr.words.unigrams.tsv dedup.tr.words.bigrams.tsv dedup.tr.words.trigrams.tsv |
| | | Wikipedia | wiki.tr.1M.vec |     54M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.tr.1M.vec | | |
| Ukrainian | uk | OpenSubtitles | subs.uk.1M.vec |   4945K | dedup.uk.words.unigrams.tsv dedup.uk.words.bigrams.tsv dedup.uk.words.trigrams.tsv |
| | | Wikipedia | wiki.uk.1M.vec |    162M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.uk.1M.vec | | |
| Urdu | ur | OpenSubtitles | subs.ur.1M.vec |    195K | dedup.ur.words.unigrams.tsv dedup.ur.words.bigrams.tsv dedup.ur.words.trigrams.tsv |
| | | Wikipedia | wiki.ur.1M.vec |     15M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.ur.1M.vec | | |
| Vietnamese | vi | OpenSubtitles | subs.vi.1M.vec |     27M | dedup.vi.words.unigrams.tsv dedup.vi.words.bigrams.tsv dedup.vi.words.trigrams.tsv |
| | | Wikipedia | wiki.vi.1M.vec |    115M | |
| | | Wikipedia + OpenSubtitles | wiki-subs.vi.1M.vec | | |
