# coding:utf-8

import logging
import argparse
import io
import os
from sep import context
from sep import nltkwrapper
from sep.service import convert
from sep.service import graph
from sep.service import ranking as rankmod

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def savecsv(filename, data):
    logger.info('save to %s', filename)
    with io.open(filename, 'w') as fio:
        for row in data:
            fio.write(u"\t".join(map(unicode, row)) + u"\n")

def graphdata():
    data = graph.load()
    savecsv(os.path.join(context.dbdir(), 'graphdata.csv'), data)

def taggedranking():
    ranks = rankmod.loadtaggedranking()
    savecsv(os.path.join(context.dbdir(), 'taggedranking.csv'), ranks)

def nnranking():
    ranks = rankmod.loadnnranking()
    savecsv(os.path.join(context.dbdir(), 'nnranking.csv'), ranks)

def cooccurence():
    ctx = context.Context()
    logger.info('vocabrary load...')
    vocab = nltkwrapper.Vocab(ctx)
    ranking = vocab.vocab(300)
    stems = vocab.stemmer.getdict().items()
    logger.info('load words coocurence...')
    cooc = vocab.cooccurence(dict(ranking).keys()).items()
    cooc.sort(lambda x,y:cmp(y[1],x[1]))
    cooc = [(k0,k1,c) for ((k0,k1),c) in cooc]
    logger.info('save...')
    savecsv(os.path.join(context.dbdir(), 'ranking.csv'), ranking)
    savecsv(os.path.join(context.dbdir(), 'cooccurence.csv'), cooc)
    savecsv(os.path.join(context.dbdir(), 'stem.csv'), stems)

def ranking():
    ctx = context.Context()
    vocab = nltkwrapper.Vocab(ctx)
    ranking = vocab.vocab(300)
    stems = vocab.stemmer.getdict().items()
    savecsv(os.path.join(context.dbdir(), 'ranking.csv'), ranking)
    savecsv(os.path.join(context.dbdir(), 'stem.csv'), stems)

commands = {
    'text': convert.iterdir,
    'ranking': ranking,
    'cooccurence': cooccurence,
    'taggedranking': taggedranking,
    'nnranking': nnranking,
    'graph': graph.graphdraw,
}

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('command')
    parser.add_argument('option', nargs='*')
    args = parser.parse_args()
    if args.option:
        commands.get(args.command)(*args.option)
    else:
        commands.get(args.command)()

if __name__ == '__main__':
    main()

