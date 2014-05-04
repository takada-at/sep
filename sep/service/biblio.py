# coding:utf-8

from collections import Counter
import os
import re
from scrapy.selector import Selector
from sep import context
from sep.lib import regbibparser

def count():
    bibs = []
    dirname = context.htmldir()
    for fpath in os.listdir(dirname):
        fullpath = os.path.join(dirname, fpath)
        if os.path.isfile(fullpath):
            bibs += handlefile(fullpath)

    return sumbibs(bibs)

def sumbibs(bibs):
    items = regbibparser.parseitems(bibs)
    counter = Counter((item.get('author', ''), item.get('year'), item.get('title')) for item in items)
    return counter

def handlefile(filepath):
    if not filepath.endswith('.html'): return []
    bibcounter = Counter()
    with open(filepath) as fio:
        html = fio.read()
        bibs = fetchbiblio(html)
        return bibs

reg = re.compile(r'<li>(.*)</li>')
def fetchbiblio(html):
    sel = Selector(text=html)
    article = sel.css('#article')
    articlestr = article.extract()[0]
    bibtitle = article.xpath('//h2[starts-with(., "Bibliography")]').extract()[0]
    actoolstitle = article.xpath('//h2[starts-with(., "Academic Tools")]').extract()[0]
    bibregion = articlestr.split(bibtitle)[1].split(actoolstitle)[0]
    sel2 = Selector(text=bibregion)
    bibtexts = []
    for li in sel2.xpath('//li'):
        string = li.extract()
        string = string.replace("\n", " ")
        bibtexts.append(string)

    return bibtexts

