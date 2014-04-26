# coding:utf-8

import argparse
import io
import os
from sep import context
from sep import nltkwrapper
from sep.ranking import saveranking
from sep.commands import graph
from sep.commands import cooccurence
    
def createranking(ctx,save=False):
    fdist = nltkwrapper.freq(ctx.collections)
    ranking = nltkwrapper.ranking(fdist, 300)
    if not save:
        return ranking

    saveranking(ranking)
    return ranking

def cooccurence():
    cooccurence.save(update=False)

def ranking():
    ctx = context.Context()
    ctx.load()
    ranking = createranking(ctx, save=True)

commands = {
    'ranking': ranking,
    'cooccurence': cooccurence,
    'graph': graph.graphdraw,
}

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('command')
    args = parser.parse_args()
    commands.get(args.command)()

if __name__ == '__main__':
    main()

