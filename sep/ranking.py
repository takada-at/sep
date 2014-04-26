# coding:utf-8
import io
import os
from sep import context
import nltk

def saveranking(ranking):
    dbdir = context.dbdir()
    with io.open(os.path.join(dbdir, 'ranking.csv'), 'w') as wio:
        for word, freq in ranking:
            wio.write(u"\t".join([word, unicode(freq)]) + u"\n")

    return ranking

def loadranking():
    dirname = context.dbdir()
    ranking = []
    with io.open(os.path.join(dirname, 'ranking.csv')) as fio:
        for line in fio:
            word,count = line.rstrip().split("\t")
            ranking.append((word, int(count)))

    return ranking

def loadtaggedranking():
    taggedranking = []
    ranking = loadranking()
    for word,count in ranking:
        word,tag = nltk.pos_tag([word])[0]
        taggedranking.append((word,tag,int(count)))

    return taggedranking

def loadnnranking():
    taggedranking = loadtaggedranking()
    return [(w[0],w[2]) for w in taggedranking if w[1].startswith('NN')]
