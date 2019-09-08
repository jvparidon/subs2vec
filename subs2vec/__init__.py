"""
subs2vec
========

Provides:
  - Routines for interacting with, evaluating, and training word embeddings as used in Van Paridon & Thompson (2019).
  - Routines for extending lexical norms to unnormed words.
  - Routines for retrieving word, bigram, and trigram frequencies.
  - Command line tools to conveniently do any of the above, in 50 languages.
"""

__author__ = "Jeroen van Paridon & Bill Thompson"
__version__ = "0.9.0"

__all__ = [
    'analogies',
    'clean_subs',
    'clean_wiki',
    'count_words',
    'deduplicate',
    'download',
    'eval_lang',
    'frequencies',
    'norms',
    'plots',
    'shuffle_text',
    'similarities',
    'train_model',
    'utensils',
    'vecs'
]
