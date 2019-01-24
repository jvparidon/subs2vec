fname = '../OpenSubtitles2018/raw/en/2017/'
#fname = '../tmp-jeroen/ar.dedup.txt'
#fname = '../tmp-jeroen/ko.dedup.txt'
#fname = '../tmp-jeroen/ko.dedup.5pass.d5.t100.utf-8.txt'
fname = '../tmp-jeroen/ko.dedup.5pass.d5.t100.utf-8.neg5.epoch5.t0.0001.300d.vec'
with open(fname, 'r', encoding='utf-8') as infile:
    i = 0
    for line in infile:
        i += 1
        #print(i)
        #if i == 78796:

# invalid line = 565161
