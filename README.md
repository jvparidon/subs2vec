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
| Afrikaans | af | OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_59a61205_dfc3_4eec_9fd9_311b3f65c9a5/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_486caf84_5d28_439c_a09f_6b90b7fe79dd/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_8d87878f_ce0b_4221_81b3_5fff04eec335/datastream/OBJ/download) |    323K | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_a1a82d13_be9d_4024_bbfe_90de100fcd3c/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_1f671cfa_131d_4fa8_bfe2_021a59952256/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_e4a8e2f0_2cfa_4d5a_8d22_864ef02d7f26/datastream/OBJ/download) |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     17M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Arabic | ar | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    188M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
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
| Kazakh | kk | OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_44ffc57f_2907_4a6d_ad8d_5cd2dbea548a/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_eb1c5733_9db5_4704_ab4c_5902f70fccb4/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_d98342a1_0d67_4f94_9b33_c7e475ccdb38/datastream/OBJ/download) |     13K | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_73557531_5ebe_4fd5_aaf7_96a328f3288c/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_b6bb4967_e417_400a_9abb_5dc3e8dcae38/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_ba79d053_a8ee_46d3_9e7f_27eaebab9cb5/datastream/OBJ/download) |
| | | Wikipedia | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_850e9909_d908_43ba_bdbc_762cfbd86cf2/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_8c3b1f6c_576c_4075_88ab_25cc4070f2be/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_1d277b69_8535_4eb7_a4e6_9c30b418a537/datastream/OBJ/download) |     18M | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_40bacff9_818d_49ad_95bc_a550fc3247d4/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_7ec6488c_21ba_4109_af84_4c437bf22200/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_5d0dd48b_6b03_4ae1_9136_526485003675/datastream/OBJ/download) |
| | | Wikipedia + OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_56778c23_b5c5_4386_83cb_29d04ad014ea/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_b7a5b672_edc3_4254_8759_98eb6404f8a3/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_b1350e33_4e2f_4288_98be_5fdacef9b00a/datastream/OBJ/download) | | |
| Korean | ko | OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_bbac0453_6c95_4c82_af67_f4909720d578/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_9bd14106_e852_4ba2_a523_88a71e2fc1a5/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_903f9539_86f7_4521_a2f8_2355f7c95a2f/datastream/OBJ/download) |   6834K | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_76a0c30c_89ea_4fd4_8eeb_e671dc855edc/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_959a996c_2796_4168_93ef_b6e410aa0a3c/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_1268820a_d32d_476c_b5b6_060914c1ea21/datastream/OBJ/download) |
| | | Wikipedia | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_e2a992e6_7cd5_4f7f_b8ac_ca17a50eae3c/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_0b635218_eca2_48f1_b2a5_260d023681f2/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_8068db80_6934_472d_8bf3_97089cbc40e3/datastream/OBJ/download) |     62M | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_f652d0b2_6653_4839_b04d_5615b8333f91/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_a572deb8_089b_4213_ac5e_e924429db33a/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_ebec81d9_4ec8_4454_ab14_d540693f720b/datastream/OBJ/download) |
| | | Wikipedia + OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_7df56c99_9d28_4cff_b451_cfaff102ed1b/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_c6c95a97_8947_4632_9585_f29030c21e17/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_dd0ee9c1_5abe_4112_b753_68427c4296eb/datastream/OBJ/download) | | |
| Lithuanian | lt | OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_f76df11e_95fb_497c_84ed_e23e2279e2e8/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_01a0e0af_d1b3_4a72_a221_7b1dd6833b14/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_350358e2_e6cd_4187_a837_652f22736bbd/datastream/OBJ/download) |   6252K | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_50610f54_6ce9_4a3d_aea5_48ffdf8f0fc1/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_f92815d5_6cf7_49ef_ae29_f969c883dd5d/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_d737ae7e_c8d9_4442_a46e_15381ba66c72/datastream/OBJ/download) |
| | | Wikipedia | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_e45287ca_f7d6_4ff8_af39_89bc903c9d55/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_aeb3c6f4_b2d3_4570_9b99_617932f6ce56/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_1e26774e_df35_4226_9d3b_4b2f0c6a845e/datastream/OBJ/download) |     23M | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_de604796_0112_4651_9cc4_24f7c6e7996f/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_ca300706_672f_41f8_9302_ef18cb860cc6/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_957139ee_80a2_44c4_8c6c_70d3ee755d07/datastream/OBJ/download) |
| | | Wikipedia + OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_c998ccca_a700_40ec_9332_25b4c6dc4363/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_eed538a6_666f_4bb0_9938_df8a79619203/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_49d1e6a5_48c0_441b_98f2_0d5c632331d3/datastream/OBJ/download) | | |
| Latvian | lv | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |   2167K | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     13M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Macedonian | mk | OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_fcb27857_3c2a_403d_bb7c_8f43ca0224ad/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_2cb685d6_ce0c_4f4c_9253_283b474a5f2a/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_180b7221_8948_41c9_b75f_3a38e8e92e18/datastream/OBJ/download) |     20M | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_faff5266_9f41_49d7_982b_643b8466782b/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_37fa5ace_cc32_4664_a592_b7d1aba46670/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_8c17fea7_410a_4c17_a289_74e2576baa73/datastream/OBJ/download) |
| | | Wikipedia | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_16ecfcd3_2900_42bd_9f97_c5dd2bd1019b/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_21df4ce4_d137_470d_a56d_c55bdd1e3245/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_0d998d85_5c31_4276_95e6_ddd1ac27a3cd/datastream/OBJ/download) |     26M | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_b21ddd7d_f887_413e_8995_2aa57498b3ea/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_8dfe1739_2504_4a0e_a44e_8d7612c76e86/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_ac8779c0_4dc9_4545_8a3e_2f7256dd488d/datastream/OBJ/download) |
| | | Wikipedia + OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_7dee4f33_5979_492e_a5ab_888d28245dbb/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_85735ca3_486e_4e21_bd23_fc39eff4a6b3/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_df65508b_fd67_4524_ba5a_1e99fa13ebf4/datastream/OBJ/download) | | |
| Malayalam | ml | OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_f6c6298f_aa9d_4dc6_8fe2_e3626d674cbd/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_3921fbc6_a509_4028_aaf0_5b31cc47e62c/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_73cd8422_228c_4ee7_ba97_c65622e3baf1/datastream/OBJ/download) |   1520K | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_1a0b6c67_30a5_451f_8b95_2a0da9c3070b/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_2d1282e3_63ac_481b_95ec_de159294df64/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_98c5650d_d771_4b44_85b5_ea9688da1778/datastream/OBJ/download) |
| | | Wikipedia | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_addecc73_8134_4437_8ea9_dca7628917b0/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_251223b4_6875_4d63_8dc8_1194360a1d86/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_04a501f1_84cf_435f_843a_c8168d789fb5/datastream/OBJ/download) |     10M | [unigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_518af478_4f8d_47ea_89a2_b8385eab3ce2/datastream/OBJ/download)<br>[bigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_e38201e2_c6a1_4ad7_a6c4_55b5fc3950ef/datastream/OBJ/download)<br>[trigrams](https://archive.mpi.nl/islandora/object/lat%3A1839_9a7c97f1_ae65_4c91_a01b_ffd147d4906a/datastream/OBJ/download) |
| | | Wikipedia + OpenSubtitles | [top 1M](https://archive.mpi.nl/islandora/object/lat%3A1839_4e5d035d_f5ae_4a62_8604_c12d5e49c629/datastream/OBJ/download)<br>[all](https://archive.mpi.nl/islandora/object/lat%3A1839_70b69424_2fd1_465e_ba4f_f3750879be8a/datastream/OBJ/download)<br>[binary](https://archive.mpi.nl/islandora/object/lat%3A1839_f77cbeb4_ac6b_46a1_86ca_bc259899b1b2/datastream/OBJ/download) | | |
| Malay | ms | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |     12M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     28M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Dutch | nl | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    264M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |    248M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Norwegian | no | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |     45M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     90M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Poland | pl | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    250M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |    232M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Portuguese | pt | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    257M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |    238M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Romanian | ro | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    434M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     65M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Russian | ru | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    152M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |    390M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Sinhalese | si | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |   3493K | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |   5980K | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Slovak | sk | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |     47M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     28M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Slovene | sl | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    106M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     31M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Albanian | sq | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |     11M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     17M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Serbian | sr | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    343M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     69M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Swedish | sv | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    101M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |    143M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Tamil | ta | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    123K | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     17M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Telugu | te | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    103K | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     15M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Thai | th | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |     10M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     12M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Tagalog | tl | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |     87K | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |   6515K | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Turkish | tr | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    239M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     54M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Ukrainian | uk | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |   4945K | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |    162M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Urdu | ur | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |    195K | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |     15M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
| Vietnamese | vi | OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() |     27M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia | [top 1M]()<br>[all]()<br>[binary]() |    115M | [unigrams]()<br>[bigrams]()<br>[trigrams]() |
| | | Wikipedia + OpenSubtitles | [top 1M]()<br>[all]()<br>[binary]() | | |
