import vecs
import os

if __name__ == '__main__':
    '''
    vecs_dir = '../for_publication'
    for lang in sorted(os.listdir(vecs_dir)):
        if '.' not in lang:
            vecs_dict = vecs.load_vecs(fname=os.path.join(vecs_dir, lang, f'sub.{lang}.vec'), normalize=True)
            vecs.evaluate_vecs(vecs_dict, lang=lang, no_analogies=True)
    '''

    vecs_dir = '../pretrained/fasttext/'
    for filename in sorted(os.listdir(vecs_dir)):
        if filename.startswith('cc'):
            lang = filename.split('.')[1]
            vecs_dict = vecs.load_vecs(fname=os.path.join(vecs_dir, filename), normalize=True)
            vecs.evaluate_vecs(vecs_dict, lang=lang, no_analogies=True)
