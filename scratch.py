import strip_wiki


with open('enwiki-20180620-pages-articles.xml', 'r', encoding='utf-8') as infile:
    #txt = infile.readlines(1000000)
    txt = infile.readlines(2000000)
    txt = ''.join(txt)

txt = strip_wiki.strip_wiki_xml(txt)
print(txt)
