from __future__ import print_function
import io
import os
import re
from sep import context
from scrapy.selector import Selector
import nltk

def iterdir():
    dirname = context.htmldir()
    for fpath in os.listdir(dirname):
        fullpath = os.path.join(dirname, fpath)
        if os.path.isfile(fullpath):
            handlefile(fullpath)

def fetcharticle(selector):
    article = selector.css('#article')
    articlestr = article.extract()[0]
    bib = article.xpath('//h2[starts-with(., "Bibliography")]').extract()[0]
    articlebody = articlestr.split(bib)[0]
    sel = Selector(text=articlebody)
    paragraphs = []
    for p in sel.xpath('(//p|//blockquote|//h1|//h2|//h3)'):
        string = p.extract()
        paragraphs.append(nltk.clean_html(string.replace("\n"," ")))

    return u"\n".join(paragraphs)

def handlefile(filepath):
    with open(filepath) as fio:
        html = fio.read()
        sel = Selector(text=html)
        article = fetcharticle(sel)
        saveconverted(article, filepath)

reg = re.compile('<[^>]*>')
def removetag(text):
    return re.sub(reg, '', text)

def saveconverted(converted, filepath):
    basename = os.path.basename(filepath).split('.')[0] + '.txt'
    savedir = context.textdatadir()
    savepath = os.path.join(savedir, basename)
    with io.open(savepath, 'w') as wio:
        print(savepath)
        wio.write(unicode(converted))

def main():
    iterdir()
    
if __name__ == '__main__':
    main()
