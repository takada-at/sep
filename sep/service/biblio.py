# coding:utf-8

from collections import Counter
import os
import re
from scrapy.selector import Selector
from sep import context
from sep.lib import regbibparser

def count():
    counter = Counter()
    dirname = context.htmldir()
    for fpath in os.listdir(dirname):
        fullpath = os.path.join(dirname, fpath)
        if os.path.isfile(fullpath):
            counter += handlefile(fullpath)

    return mergeauthors(counter)

initial = re.compile('[A-Z]\.')
def mergeauthors(dic):
    newdict = Counter()
    authors = set(dic.keys())
    for key,val in dic.iteritems():
        aut = key[0]
        if not aut:continue
        names = aut.split(' ')
        fname = names[0]
        if not fname:
            continue
        if '.' in fname:
            continue

        ini = fname[0] + '.'
        ininame = u' '.join([ini] + names[1:])
        key2 = (ininame, key[1], key[2])
        if key2 in dic:
            newdict[key] += val
            newdict[key] += dic[key2]
            try:
                authors.remove(key)
                authors.remove(key2)
            except:
                key,key2

    for key in authors:
        newdict[key] = dic[key]

    return newdict

def handlefile(filepath):
    bibcounter = Counter()
    with open(filepath) as fio:
        html = fio.read()
        bibs = fetchbiblio(html)
        for bib in bibs:
            bibcounter[tuple(bib)] += 1

    return bibcounter

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

    items = regbibparser.parseitems(bibtexts)
    return [(item.get('author', ''), item.get('year'), item.get('title')) for item in items]


