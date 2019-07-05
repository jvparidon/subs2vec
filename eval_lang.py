import vecs
import os
import argparse
import norms

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('lang')
    args = argparser.parse_args()

    lang = args.lang

    langs = os.listdir('evaluation/similarities') + os.listdir('evaluation/analogies') + os.listdir('evaluation/norms')
    langs = set([lang[0:2] for lang in langs])

    filepaths = [f'../pretrained/fasttext/cc.{lang}.300.vec',
                 f'../data/wiki-sub/{lang}/wiki-sub.{lang}.vec',
                 f'../data/OpenSubtitles/raw/{lang}/sub.{lang}.vec',
                 f'../data/wiki/{lang}/wiki.{lang}.vec']
    for filepath in filepaths:
        if os.path.exists(filepath) and (lang in langs):
            print(filepath.split('/')[-1])
            norms.evaluate_vecs(lang, filepath)
            #vecs_dict = vecs.load_vecs(fname=filepath, normalize=True, n=1e6)
            #vecs.evaluate_vecs(vecs_dict, lang=lang, no_analogies=True)
            #vecs_dict = vecs.load_vecs(fname=filepath, normalize=True, n=2e5)
            #vecs.evaluate_vecs(vecs_dict, lang=lang, no_similarities=True)
