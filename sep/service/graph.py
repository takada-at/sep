# coding:utf-8
from collections import Counter
import io
import networkx
import os
import matplotlib.pyplot as plt
from random import random
import nltk
from sep import nltkwrapper
from sep import context
from sep.service import ranking

def load():
    stemmer = ranking.loadorgword()
    ranks = ranking.loadnnranking(stemmer)
    rankdict = dict(ranks)
    words = set(w[0] for w in ranks)
    dbdir = context.dbdir()
    edges = []
    with io.open(os.path.join(dbdir,'cooccurence.csv')) as fio:
        for line in fio:
            word0,word1,count = line.rstrip().split("\t")
            word0 = stemmer.orgword(word0)
            word1 = stemmer.orgword(word1)
            if word0 in words and word1 in words:
                edges.append((word0,word1,int(count)))

    edges.sort(lambda x,y:cmp(y[2],x[2]))
    edges = [(w0,w1,k) for (w0,w1,k) in edges if k>3000]
    return (edges, rankdict)

def loadgraph():
    edges,countdata = load()
    graph = networkx.Graph()
    for word0,word1,weight in edges:
        graph.add_node(word0, count=countdata[word0])
        graph.add_node(word1, count=countdata[word1])
        graph.add_edge(word0,word1,weight=weight*0.0001, count=weight)

    return graph

def color(degree):
    if degree < 5:
        return (0.7,0.7,0.9)
    elif degree < 10:
        return (0.2,0.6,0.6)
    else:
        return (0.9,0.2,0.9)
def graphdraw(targetword=None, filename=None):
    graph = loadgraph()
    nodelist = graph.nodes()
    if targetword:
        graph = networkx.ego_graph(graph, targetword)
    
    colors = [color(deg) for n,deg in networkx.degree(graph).items()]
    size = [attr['count']/5.0 for k,attr in graph.nodes(data=True)]
    width = [attr['count']/1000.0 for n0,n1,attr in graph.edges(data=True)]

    plt.figure(3,figsize=(12,12))
    pos = networkx.spring_layout(graph, scale=2.0)
    networkx.draw_networkx_nodes(graph, pos, node_size = size, node_color=colors, alpha=0.8)
    networkx.draw_networkx_edges(graph, pos, width = width, alpha=0.5)
    networkx.draw_networkx_labels(graph, pos, font_size = 12, font_family = 'sans-serif')

    plt.xticks([])
    plt.yticks([])
    dirname = context.graphdir()

    if filename is None: filename='graph.gif'
    plt.savefig(os.path.join(dirname, filename))
