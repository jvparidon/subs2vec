def link_phrases(in_fname, adjectives):
    out_fname = in_fname.replace('.txt', '.linked.txt')
    with open(in_fname, 'r', encoding='utf-8', errors='replace') as infile, open(out_fname, 'w') as outfile:
        j = 0
        for line in infile:
            line = line.strip('\n').split(' ')
            for i in range(len(line) - 1):
                if line[i] in adjectives:
                    if j % 2 == 0:
                        line[i] = '{}_{}'.format(line[i], line[i + 1])
                        line[i + 1] = ''
                    j += 1
            outfile.write('{}\n'.format(' '.join(line)))
    print('{} relevant adjectives found'.format(j))


if __name__ == '__main__':
    adjectives = ['red',
                  'blue',
                  'green',
                  'yellow',
                  'brown',
                  'pink',
                  'white',
                  'gray',
                  'black']
    fname = '../tmp-jeroen/en.dedup.5pass.d5.t100.txt'
    link_phrases(fname, adjectives)
