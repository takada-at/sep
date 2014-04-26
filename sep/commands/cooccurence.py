# coding:utf-8

import argparse
from collections import Counter
import io
import os
from sep import nltkwrapper
from sep import context

def save(update=False):
    ctx = context.Context()
    if update:
        ctx.load()
        ranking = createranking(ctx, save=True)
    else:
        ranking = context.loadranking()

    if not ranking:
        raise Exception('empty terms')

    counter = countoccurence(ranking)
    dbdir = context.dbdir()
    with io.open(os.path.join(dbdir, 'cooccurence.csv'), 'w') as wio:
        for ((t0,t1),v) in counter.iteritems():
            wio.write(u"\t".join([t0,t1,unicode(v)]) + u"\n")

    return ranking

def countoccurence(ranking):
    terms = [k for k,v in ranking]
    counter = Counter()
    for article in context.articles():
        for para in nltkwrapper.paragraphs(article):
            _countoccurencepara(para, counter, terms)

    return counter

def _countoccurencepara(paragraph, counter, terms):
    tokens = set(word.lower() for word in paragraph)
    for i,term0 in enumerate(terms):
        for j in range(i+1,len(terms)):
            term1 = terms[j]
            if term0 in tokens and term1 in tokens:
                counter[(term0, term1)] += 1

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--update', dest='update', action='store_true')
    args = parser.parse_args()
    save(args.update)

if __name__ == '__main__':
    main()
