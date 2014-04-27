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

    stemmer = Stem()
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

def create_normalized_ranking(stemmer=None):
    if stemmer is None:
        stemmer = nltkwrapper.Stem()

    counter = Counter()
    ranking = loadranking()
    for word, count in ranking:
        stem = stemmer.stem(word)
        counter[stem] += count

    rank = counter.items()
    rank.sort(lambda x,y:cmp(y[1],x[1]))
    return (rank,stemmer)

def loadtaggedranking(stemmer=None):
    taggedranking = []
    ranking,stemmer = create_normalized_ranking(stemmer=None)
    for stem,count in ranking:
        word = stemmer.orgword(stem)
        word,tag = nltk.pos_tag([word])[0]
        taggedranking.append((word,tag,int(count)))

    return taggedranking

def loadnnranking(stemmer=None):
    taggedranking = loadtaggedranking(stemmer=None)
    return [(w[0],w[2]) for w in taggedranking if w[1]=='NN']
