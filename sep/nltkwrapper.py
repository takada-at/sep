# coding:utf-8

import csv
import io
from collections import defaultdict
import os
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.probability import ConditionalFreqDist as CFD

class ParagraphIndex():
    def __init__(self, rawtexts, normalizer, paragraph_func=None):
        if paragraph_func is None: paragraph_func=paragraphs
        tk2p = CFD((normalizer.normalize(token), (i,j))
                   for i,article in enumerate(rawtexts)
                   for j,para in enumerate(paragraph_func(article))
                   for token in para if normalizer.ok(token))
        self._tk2p = tk2p

    def score(self, words):
        fd = self.common_paragraphs(words)
        return sum(fd.values())

    def common_paragraphs(self, words):
        paragraphs = [set(self._tk2p[w]) for w in words]
        common = reduce(set.intersection, paragraphs)
        if not common:
            return FreqDist()

        fd = FreqDist(c for w in words
                      for c in self._tk2p[w]
                      if c in common)
        return fd
        
class Stem():
    # der Naturのせいでおかしくなるので上書き
    dic = {
        'natur': 'nature',
        'philosophe': 'philosopher',
        }
    def __init__(self):
        self.stemmer = nltk.PorterStemmer()
        self._orgwords = defaultdict(set)
    def getdict(self):
        return dict((k,self.orgword(k)) for k in self._orgwords.iterkeys())
    def stem(self,word):
        stem = self.stemmer.stem(word)
        self._orgwords[stem].add(word)
        return stem
    def loaddata(self,data):
        for key,item in data.iteritems():
            self._orgwords[key].add(item)
    def orgword(self,stem):
        if stem in self.dic: return self.dic[stem]
        orgs = list(self._orgwords[stem])
        orgs.sort(lambda x,y:cmp(len(x),len(y)))
        return orgs[0]

class Vocab():
    def __init__(self,ctx):
        self.ctx = ctx
        self.stemmer = Stem()
        self._fdist = None
        self._index = None
    def _createindex(self):
        normalizer = Normalizer(stemmer=self.stemmer)
        self._index = ParagraphIndex(self.ctx.rawtexts, normalizer, sencences)
    def cooccurence(self, words):
        if not self._index: self._createindex()
        d = FreqDist()
        for i,word0 in enumerate(words):
            for word1 in words[i+1:]:
                score = self._index.score([word0,word1])
                if score>0:
                    d[(word0,word1)] = score

        return d
    def _createfdist(self):
        normalizer = Normalizer(stemmer=self.stemmer)
        self.ctx.load()
        self.words = [normalizer.normalize(word) for word in self.ctx.collections if normalizer.ok(word)]
        self._fdist = nltk.FreqDist(self.words)
        self.normalizer = normalizer
    def vocab(self, num=100):
        if not self._fdist: self._createfdist()
        res = []
        for key, val in self._fdist.iteritems():
            res.append((key,val))
            if len(res)>=num:
                return res

        return res
    
def createtext(string):
    tokens = nltk.wordpunct_tokenize(string)
    return nltk.text.Text(tokens)
    
def ranking(fdist, num=100):
    res = []
    for key, val in fdist.iteritems():
        res.append((key,val))
        if len(res)>=num:
            return res

def paragraphs(article):
    paragraphs = []
    for para in article.split(u"\n"):
        if para==u"":
            continue

        tokens = nltk.wordpunct_tokenize(para)
        if len(tokens)>0:
            paragraphs.append(tokens)

    return paragraphs

def sencences(article):
    paragraphs = []
    for para in article.split(u"\n"):
        if para==u"":
            continue

        paragraphs += [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(para)]

    return paragraphs

class Normalizer():
    def __init__(self,stemmer=None):
        self.ignored_words = set(stopwords.words('english'))
        if stemmer is None: stemmer=Stem()
        self.stemmer = stemmer
    def normalizetokens(self, tokens):
        return [self.normalize(token) for token in tokens if self.ok(token)]
    def ok(self, word):
        return len(word) > 3 and word.isalpha() and word not in self.ignored_words
    def normalize(self, word):
        return self.stemmer.stem(word.lower())

