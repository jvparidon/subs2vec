import random


def shuffle_text(fname):
    with open(fname, 'r', encoding='utf-8', errors='replace') as infile, open(fname + '.shuffled', 'w', encoding='utf-8') as outfile:
        print('reading text from {}'.format(fname))
        text = infile.read()
        print('finished reading text, starting split')
        text = text.split(' ')
        print('finished splitting, starting shuffle')
        random.shuffle(text)
        print('finished shuffling, starting join')
        text = ' '.join(text)
        print('finished joining, starting write')
        outfile.write(text)
        print('finished writing')


if __name__ == '__main__':
    fname = '../tmp-jeroen/en.dedup.5pass.d5.t100.txt'
    shuffle_text(fname)
