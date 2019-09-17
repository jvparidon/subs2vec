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

## Datasets

| language | lang | corpus | vectors | corpus word count | ngram frequencies |
|---|---|---|---|---:|---|
| Afrikaans | af | OpenSubtitles | ../../data/OpenSubtitles/raw/af/dedup.af.txt | 323664 | |
| | | | | | |
| | | | | | |
| | | Wikipedia | ../../data/wiki/af/dedup.afwiki-meta.txt | 17089024
| Arabic | ar | OpenSubtitles | ../../data/OpenSubtitles/raw/ar/dedup.ar.txt | 188360588 | |
| | | | | | |
| | | | | | |
| | | Wikipedia | ../../data/wiki/ar/dedup.arwiki-meta.txt | 119823113
| Bulgarian | bg | OpenSubtitles | ../../data/OpenSubtitles/raw/bg/dedup.bg.txt | 246937673
| | | | | | 
| | | | | | 
| | | Wikipedia | ../../data/wiki/bg/dedup.bgwiki-meta.txt | 53474662
| Bengali | bn | OpenSubtitles | ../../data/OpenSubtitles/raw/bn/dedup.bn.txt | 2227540
| | | | | | 
| | | | | | 
| | | Wikipedia | ../../data/wiki/bn/dedup.bnwiki-meta.txt | 18575527
| Breton | br | OpenSubtitles | ../../data/OpenSubtitles/raw/br/dedup.br.txt | 110928
| | | | | | 
| | | | | | 
| | | Wikipedia | ../../data/wiki/br/dedup.brwiki-meta.txt | 7644078
| Bosnian | bs | OpenSubtitles | ../../data/OpenSubtitles/raw/bs/dedup.bs.txt | 91932338
| | | | | | 
| | | | | | 
| | | Wikipedia | ../../data/wiki/bs/dedup.bswiki-meta.txt | 13140964
| Catalan | ca | OpenSubtitles | ../../data/OpenSubtitles/raw/ca/dedup.ca.txt | 3098951
| | | | | | 
| | | | | | 
| | | Wikipedia | ../../data/wiki/ca/dedup.cawiki-meta.txt | 175562502
| Czech | cs | OpenSubtitles | ../../data/OpenSubtitles/raw/cs/dedup.cs.txt | 249041681
| | | | | | 
| | | | | | 
| | | Wikipedia | ../../data/wiki/cs/dedup.cswiki-meta.txt | 100293683
| Danish | da | OpenSubtitles | ../../data/OpenSubtitles/raw/da/dedup.da.txt | 87088175
| | | | | | 
| | | | | | 
| Danish | da | Wikipedia | ../../data/wiki/da/dedup.dawiki-meta.txt | 56246020
| German | de | OpenSubtitles | ../../data/OpenSubtitles/raw/de/dedup.de.txt | 139494247
| | | | | | 
| | | | | | 
| German | de | Wikipedia | ../../data/wiki/de/dedup.dewiki-meta.txt | 976143003
| Greek | el | OpenSubtitles | ../../data/OpenSubtitles/raw/el/dedup.el.txt | 271063438
| | | | | | 
| | | | | | 
| Greek | el | Wikipedia | ../../data/wiki/el/dedup.elwiki-meta.txt | 58228906
| English | en | OpenSubtitles | ../../data/OpenSubtitles/raw/en/dedup.en.txt | 750595864
| | | | | | 
| | | | | | 
| English | en | Wikipedia | ../../data/wiki/en/dedup.enwiki-meta.txt | 2477794991
| Esperanto | eo | OpenSubtitles | ../../data/OpenSubtitles/raw/eo/dedup.eo.txt | 381667
| | | | | | 
| | | | | | 
| Esperanto | eo | Wikipedia | ../../data/wiki/eo/dedup.eowiki-meta.txt | 37640320
| Spanish | es | OpenSubtitles | ../../data/OpenSubtitles/raw/es/dedup.es.txt | 514363934
| | | | | | 
| | | | | | 
| Spanish | es | Wikipedia | ../../data/wiki/es/dedup.eswiki-meta.txt | 585587692
| Estonian | et | OpenSubtitles | ../../data/OpenSubtitles/raw/et/dedup.et.txt | 60427435
| | | | | | 
| | | | | | 
| Estonian | et | Wikipedia | ../../data/wiki/et/dedup.etwiki-meta.txt | 29174555
| Basque | eu | OpenSubtitles | ../../data/OpenSubtitles/raw/eu/dedup.eu.txt | 3400495
| | | | | | 
| | | | | | 
| Basque | eu | Wikipedia | ../../data/wiki/eu/dedup.euwiki-meta.txt | 20139779
| Farsi | fa | OpenSubtitles | ../../data/OpenSubtitles/raw/fa/dedup.fa.txt | 45332894
| | | | | | 
| | | | | | 
| Farsi | fa | Wikipedia | ../../data/wiki/fa/dedup.fawiki-meta.txt | 86730262
| Finnish | fi | OpenSubtitles | ../../data/OpenSubtitles/raw/fi/dedup.fi.txt | 116907162
| | | | | | 
| | | | | | 
| Finnish | fi | Wikipedia | ../../data/wiki/fi/dedup.fiwiki-meta.txt | 73628518
| French | fr | OpenSubtitles | ../../data/OpenSubtitles/raw/fr/dedup.fr.txt | 335525382
| | | | | | 
| | | | | | 
| French | fr | Wikipedia | ../../data/wiki/fr/dedup.frwiki-meta.txt | 724280677
| Galician | gl | OpenSubtitles | ../../data/OpenSubtitles/raw/gl/dedup.gl.txt | 1666743
| | | | | | 
| | | | | | 
| Galician | gl | Wikipedia | ../../data/wiki/gl/dedup.glwiki-meta.txt | 40154890
| Hebrew | he | OpenSubtitles | ../../data/OpenSubtitles/raw/he/dedup.he.txt | 169640986
| | | | | | 
| | | | | | 
| Hebrew | he | Wikipedia | ../../data/wiki/he/dedup.hewiki-meta.txt | 132900287
| Hindi | hi | OpenSubtitles | ../../data/OpenSubtitles/raw/hi/dedup.hi.txt | 659798
| | | | | | 
| | | | | | 
| Hindi | hi | Wikipedia | ../../data/wiki/hi/dedup.hiwiki-meta.txt | 31099477
| Croatian | hr | OpenSubtitles | ../../data/OpenSubtitles/raw/hr/dedup.hr.txt | 241661205
| | | | | | 
| | | | | | 
| Croatian | hr | Wikipedia | ../../data/wiki/hr/dedup.hrwiki-meta.txt | 42982505
| Hungarian | hu | OpenSubtitles | ../../data/OpenSubtitles/raw/hu/dedup.hu.txt | 227698561
| | | | | | 
| | | | | | 
| Hungarian | hu | Wikipedia | ../../data/wiki/hu/dedup.huwiki-meta.txt | 120830242
| Armenian | hy | OpenSubtitles | ../../data/OpenSubtitles/raw/hy/dedup.hy.txt | 23730
| | | | | | 
| | | | | | 
| Armenian | hy | Wikipedia | ../../data/wiki/hy/dedup.hywiki-meta.txt | 38490279
| Indonesian | id | OpenSubtitles | ../../data/OpenSubtitles/raw/id/dedup.id.txt | 65035949
| | | | | | 
| | | | | | 
| Indonesian | id | Wikipedia | ../../data/wiki/id/dedup.idwiki-meta.txt | 69226947
| Icelandic | is | OpenSubtitles | ../../data/OpenSubtitles/raw/is/dedup.is.txt | 7474111
| | | | | | 
| | | | | | 
| Icelandic| is | Wikipedia | ../../data/wiki/is/dedup.iswiki-meta.txt | 7196891
| Italian | it | OpenSubtitles | ../../data/OpenSubtitles/raw/it/dedup.it.txt | 277692790
| | | | | | 
| | | | | | 
| Italian | it | Wikipedia | ../../data/wiki/it/dedup.itwiki-meta.txt | 476457198
| Japanese | ja | OpenSubtitles | ../../data/OpenSubtitles/raw/ja/dedup.ja.txt | 3027883
| | | | | | 
| | | | | | 
| Japanese | ja | Wikipedia | ../../data/wiki/ja/dedup.jawiki-meta.txt | 23524347
| Georgian | ka | OpenSubtitles | ../../data/OpenSubtitles/raw/ka/dedup.ka.txt | 1108570
| | | | | | 
| | | | | | 
| Georgian | ka | Wikipedia | ../../data/wiki/ka/dedup.kawiki-meta.txt | 15259793
| Kazakh | kk | OpenSubtitles | ../../data/OpenSubtitles/raw/kk/dedup.kk.txt | 13480
| | | | | | 
| | | | | | 
| Kazakh | kk | Wikipedia | ../../data/wiki/kk/dedup.kkwiki-meta.txt | 18298523
| Korean | ko | OpenSubtitles | ../../data/OpenSubtitles/raw/ko/dedup.ko.txt | 6834406
| | | | | | 
| | | | | | 
| Korean | ko | Wikipedia | ../../data/wiki/ko/dedup.kowiki-meta.txt | 62946030
| Lithuanian | lt | OpenSubtitles | ../../data/OpenSubtitles/raw/lt/dedup.lt.txt | 6252008
| | | | | | 
| | | | | | 
| Lithuanian | lt | Wikipedia | ../../data/wiki/lt/dedup.ltwiki-meta.txt | 23201287
| Latvian | lv | OpenSubtitles | ../../data/OpenSubtitles/raw/lv/dedup.lv.txt | 2167620
| | | | | | 
| | | | | | 
| Latvian | lv | Wikipedia | ../../data/wiki/lv/dedup.lvwiki-meta.txt | 13939982
| Macedonian | mk | OpenSubtitles | ../../data/OpenSubtitles/raw/mk/dedup.mk.txt | 20095253
| | | | | | 
| | | | | | 
| Macedonian | mk | Wikipedia | ../../data/wiki/mk/dedup.mkwiki-meta.txt | 26681024
| Malayalam | ml | OpenSubtitles | ../../data/OpenSubtitles/raw/ml/dedup.ml.txt | 1520820
| | | | | | 
| | | | | | 
| Malayalam | ml | Wikipedia | ../../data/wiki/ml/dedup.mlwiki-meta.txt | 10454147
| Malay | ms | OpenSubtitles | ../../data/OpenSubtitles/raw/ms/dedup.ms.txt | 12184059
| | | | | | 
| | | | | | 
| Malay | ms | Wikipedia | ../../data/wiki/ms/dedup.mswiki-meta.txt | 28946522
| Dutch | nl | OpenSubtitles | ../../data/OpenSubtitles/raw/nl/dedup.nl.txt | 264868501
| | | | | | 
| | | | | | 
| Dutch | nl | Wikipedia | ../../data/wiki/nl/dedup.nlwiki-meta.txt | 248764425
| Norwegian | no | OpenSubtitles | ../../data/OpenSubtitles/raw/no/dedup.no.txt | 45553185
| | | | | | 
| | | | | | 
| Norwegian | no | Wikipedia | ../../data/wiki/no/dedup.nowiki-meta.txt | 90882902
| Polish | pl | OpenSubtitles | ../../data/OpenSubtitles/raw/pl/dedup.pl.txt | 250390754
| | | | | | 
| | | | | | 
| Polish | pl | Wikipedia | ../../data/wiki/pl/dedup.plwiki-meta.txt | 232421847
| Portuguese | pt | OpenSubtitles | ../../data/OpenSubtitles/raw/pt/dedup.pt.txt | 257597148
| | | | | | 
| | | | | | 
| Portuguese | pt | Wikipedia | ../../data/wiki/pt/dedup.ptwiki-meta.txt | 238221600
| Romanian | ro | OpenSubtitles | ../../data/OpenSubtitles/raw/ro/dedup.ro.txt | 434898200
| | | | | | 
| | | | | | 
| Romanian | ro | Wikipedia | ../../data/wiki/ro/dedup.rowiki-meta.txt | 65168414
| Russian | ru | OpenSubtitles | ../../data/OpenSubtitles/raw/ru/dedup.ru.txt | 152197702
| | | | | | 
| | | | | | 
| Russian | ru | Wikipedia | ../../data/wiki/ru/dedup.ruwiki-meta.txt | 390749248
| Sinhalese | si | OpenSubtitles | ../../data/OpenSubtitles/raw/si/dedup.si.txt | 3493085
| | | | | | 
| | | | | | 
| Sinhalese | si | Wikipedia | ../../data/wiki/si/dedup.siwiki-meta.txt | 5980385
| Slovak | sk | OpenSubtitles | ../../data/OpenSubtitles/raw/sk/dedup.sk.txt | 47349588
| | | | | | 
| | | | | | 
| Slovak | sk | Wikipedia | ../../data/wiki/sk/dedup.skwiki-meta.txt | 28569119
| Slovene | sl | OpenSubtitles | ../../data/OpenSubtitles/raw/sl/dedup.sl.txt | 106593590
| | | | | | 
| | | | | | 
| Slovene | sl | Wikipedia | ../../data/wiki/sl/dedup.slwiki-meta.txt | 31642018
| Albanian | sq | OpenSubtitles | ../../data/OpenSubtitles/raw/sq/dedup.sq.txt | 11767480
| | | | | | 
| | | | | | 
| Albanian | sq | Wikipedia | ../../data/wiki/sq/dedup.sqwiki-meta.txt | 17768079
| Serbian | sr | OpenSubtitles | ../../data/OpenSubtitles/raw/sr/dedup.sr.txt | 343517730
| | | | | | 
| | | | | | 
| Serbian | sr | Wikipedia | ../../data/wiki/sr/dedup.srwiki-meta.txt | 69719972
| Swedish | sv | OpenSubtitles | ../../data/OpenSubtitles/raw/sv/dedup.sv.txt | 101270590
| | | | | | 
| | | | | | 
| Swedish | sv | Wikipedia | ../../data/wiki/sv/dedup.svwiki-meta.txt | 143268105
| Tamil | ta | OpenSubtitles | ../../data/OpenSubtitles/raw/ta/dedup.ta.txt | 123487
| | | | | | 
| | | | | | 
| Tamil | ta | Wikipedia | ../../data/wiki/ta/dedup.tawiki-meta.txt | 17143983
| Telugu | te | OpenSubtitles | ../../data/OpenSubtitles/raw/te/dedup.te.txt | 103117
| | | | | | 
| | | | | | 
| Telugu | te | Wikipedia | ../../data/wiki/te/dedup.tewiki-meta.txt | 15246610
| Thai | th | OpenSubtitles | ../../data/OpenSubtitles/raw/th/dedup.th.txt | 10557949
| | | | | | 
| | | | | | 
| Thai | th | Wikipedia | ../../data/wiki/th/dedup.thwiki-meta.txt | 12440033
| Tagalog | tl | OpenSubtitles | ../../data/OpenSubtitles/raw/tl/dedup.tl.txt | 87946
| | | | | | 
| | | | | | 
| Tagalog | tl | Wikipedia | ../../data/wiki/tl/dedup.tlwiki-meta.txt | 6515000
| Turkish | tr | OpenSubtitles | ../../data/OpenSubtitles/raw/tr/dedup.tr.txt | 239771328
| | | | | | 
| | | | | | 
| Turkish | tr | Wikipedia | ../../data/wiki/tr/dedup.trwiki-meta.txt | 54731119
| Ukrainian | uk | OpenSubtitles | ../../data/OpenSubtitles/raw/uk/dedup.uk.txt | 4945827
| | | | | | 
| | | | | | 
| Ukrainian | uk | Wikipedia | ../../data/wiki/uk/dedup.ukwiki-meta.txt | 162630341
| Urdu | ur | OpenSubtitles | ../../data/OpenSubtitles/raw/ur/dedup.ur.txt | 195581
| | | | | | 
| | | | | | 
| Urdu | ur | Wikipedia | ../../data/wiki/ur/dedup.urwiki-meta.txt | 15878600
| Vietnamese | vi | OpenSubtitles | ../../data/OpenSubtitles/raw/vi/dedup.vi.txt | 27372811
| | | | | | 
| | | | | | 
| Vietnamese | vi | Wikipedia | ../../data/wiki/vi/dedup.viwiki-meta.txt | 115161096