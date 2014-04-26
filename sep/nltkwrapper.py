# coding:utf-8

import csv
import io
from collections import defaultdict
import os
import nltk

def createtext(string):
    tokens = nltk.word_tokenize(string)
    return nltk.text.Text(tokens)
    
def ranking(fdist, num=100):
    res = []
    for key, val in fdist.iteritems():
        res.append((key,val))
        if len(res)>=num:
            return res

def freq(texts):
    fdist = nltk.FreqDist(word.lower() for word in texts if len(word)>3)
    return fdist

def paragraphs(article):
    for para in article.split(u"\n"):
        if para==u"":
            continue

        tokens = nltk.word_tokenize(para)
        if len(tokens)>0:
            yield tokens

