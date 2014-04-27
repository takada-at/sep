# coding:utf-8
from collections import defaultdict
from collections import Counter
import io
import os
from sep import context
from sep import nltkwrapper
import nltk

def saveranking(ranking):
    dbdir = context.dbdir()
    with io.open(os.path.join(dbdir, 'ranking.csv'), 'w') as wio:
        for word, freq in ranking:
            wio.write(u"\t".join([word, unicode(freq)]) + u"\n")

    return ranking

def loadorgword():
    dirname = context.dbdir()
    dic = dict()
    with io.open(os.path.join(dirname, 'stem.csv')) as fio:
        for line in fio:
            stem,org = line.rstrip().split("\t")
            dic[stem] = org

    stemmer = nltkwrapper.Stem()
    stemmer.loaddata(dic)
    return stemmer
    
def loadranking():
    dirname = context.dbdir()
    ranking = []
    with io.open(os.path.join(dirname, 'ranking.csv')) as fio:
        for line in fio:
            word,count = line.rstrip().split("\t")
            ranking.append((word, int(count)))

    return ranking

def create_orgword_ranking(stemmer=None):
    if stemmer is None:
        stemmer = loadorgword()

    ranking = loadranking()
    ranking = [(stemmer.orgword(w), c) for w,c in ranking]
    return (ranking,stemmer)

def loadtaggedranking(stemmer=None):
    taggedranking = []
    ranking,stemmer = create_orgword_ranking(stemmer=stemmer)
    for word,count in ranking:
        word,tag = nltk.pos_tag([word])[0]
        taggedranking.append((word,tag,int(count)))

    return taggedranking

def loadnnranking(stemmer=None):
    taggedranking = loadtaggedranking(stemmer=stemmer)
    return [(w[0],w[2]) for w in taggedranking if w[1]=='NN']
