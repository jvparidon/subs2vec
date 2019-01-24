import sub2vec

for year in range(1940, 2020, 10):
    sub2vec.generate(lang='en',
                     subs_dir='../OpenSubtitles2018',
                     no_strip=True,
                     no_join=False,
                     no_dedup=False,
                     phrase_pass=5,
                     cores=80,
                     subset_years=(year, year + 10))
