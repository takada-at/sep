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

def preparedir():
    dirs = [context.datadir(), context.graphdir(), context.dbdir(), context.textdatadir()]
    for dirname in dirs:
        if not os.path.exists(dirname):
            os.mkdir(dirname)

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

def _execute_simple(args):
    args.func()
def main():
    parser = argparse.ArgumentParser(description='generate somedata')
    subpersers = parser.add_subparsers(title='commands')
    for command in ('text','ranking','cooccurence', 'taggedranking'):
        com = subpersers.add_parser(command)
        com.set_defaults(func=commands[command])

    graphperser = subpersers.add_parser('graph')
    graphperser.add_argument('-w', '--targetword', default=None, dest='targetword')
    graphperser.add_argument('-o', '--filename', default=None, dest='filename')
    graphperser.add_argument('-l', '--limit', default=1300, dest='limit', help='minimum co-occurence', type=int)
    graphperser.add_argument('--weighted', action='store_true', dest='weighted')
    graphperser.set_defaults(func=graph.graphdraw)

    preparedir()
    args = parser.parse_args()
    opt = dict(vars(args))
    del(opt['func'])
    args.func(**opt)

if __name__ == '__main__':
    main()

