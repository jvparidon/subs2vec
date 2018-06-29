# sub2vec
Tools for training word2vec style models on a subtitle corpus

sub2vec.py is a Python3 command line tool that takes an OpenSubtitles archive and goes through all the steps to create a fastText model from the subtitle data.  
Requires utensilities, fastText and word2vec.  

Pretrained models are forthcoming, watch this space.  
If you use sub2vec and/or pretrained models, please cite the arXiv paper (also forthcoming).  
(And if you use OpenSubtitles data please credit the OpenSubtitles.org team.)

## Usage examples
To evaluate word vectors on a set of language-specific benchmarks:  
`python3 vecs.py --filename=my_spanish_vectors.vec --lang=es` (sub2vec uses the ISO 639-1 language codes)  
For more detailed evaluation options:  
`python3 vecs.py --help`

To train a sub2vec model:  
`python3 sub2vec.py --subs_dir=../OpenSubtitles2018 --lang=es`  
For more detailed training options:  
`python3 sub2vec.py --help`
