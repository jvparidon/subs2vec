import os

for lang in os.listdir('vectors/'):
    lang = lang.replace('.vec', '').replace('sub.', '')
    os.mkdir(lang)
    os.rename('vectors/sub.' + lang + '.vec', lang + '/sub.' + lang + '.vec')
    os.rename('model_binaries/sub.' + lang + '.bin', lang + '/sub.' + lang + '.bin')
