import vecs
import os

if __name__ == '__main__':
    '''
    vecs_dir = '../for_publication'
    for lang in reversed(sorted(os.listdir(vecs_dir))):
        if '.' not in lang:
            vecs_dict = vecs.load_vecs(fname=os.path.join(vecs_dir, lang, f'sub.{lang}.vec'), normalize=True, n=2e5)
            vecs.evaluate_vecs(vecs_dict, lang=lang, no_similarities=True)
    '''

    vecs_dir = '../pretrained/fasttext/'
    for filename in sorted(os.listdir(vecs_dir)):
        if filename.startswith('cc'):
            lang = filename.split('.')[1]
            vecs_dict = vecs.load_vecs(fname=os.path.join(vecs_dir, filename), normalize=True, n=2e5)
            vecs.evaluate_vecs(vecs_dict, lang=lang, no_similarities=True)
