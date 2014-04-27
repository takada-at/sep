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
from sep import ranking

def load():
    stemmer = nltkwrapper.Stem()
    ranks = ranking.loadnnranking(stemmer)
    rankdict = dict(ranks)
    words = set(stemmer.stem(w[0]) for w in ranks)
    dbdir = context.dbdir()
    edges = Counter()
    cache = set()
    with io.open(os.path.join(dbdir,'cooccurence.csv')) as fio:
        for line in fio:
            word0,word1,count = line.rstrip().split("\t")
            stem0 = stemmer.stem(word0)
            stem1 = stemmer.stem(word1)
            key0,key1 = sorted((word0, word1))
            key = (key0,key1)
            if key in cache: continue
            cache.add(key)
            if stem0 in words and stem1 in words:
                orgword0 = stemmer.orgword(stem0)
                orgword1 = stemmer.orgword(stem1)
                edges[(orgword0, orgword1)] += int(count)

    edges = [(w0,w1,v) for ((w0,w1),v) in edges.items()]
    edges.sort(lambda x,y:cmp(y[2],x[2]))
    return (edges[:200], rankdict)

def loadgraph():
    edges,countdata = load()
    graph = networkx.Graph()
    for word0,word1,weight in edges:
        graph.add_node(word0, count=countdata[word0])
        graph.add_node(word1, count=countdata[word1])
        graph.add_edge(word0,word1,weight=weight*0.002, count=weight)

    return graph
    
def graphdraw():
    graph = loadgraph()
    #networkx.draw_circular(graph)
    #networkx.draw(graph)
    colors = [(random(), random(), random()) for _i in range(10)]
    pos = networkx.spring_layout(graph)
    networkx.draw_networkx_nodes(graph, pos, node_size = 100, node_color=colors, alpha=0.8)
    networkx.draw_networkx_edges(graph, pos, width = 1, alpha=0.5)
    networkx.draw_networkx_labels(graph, pos, font_size = 12, font_family = 'sans-serif')
    plt.xticks([])
    plt.yticks([])

    networkx.write_gml(graph,'file.gml')
    plt.savefig('graph.gif')
    graph.dump(io.open('graph.json','w'))
    networkx.draw_graphviz(graph)
    networkx.write_dot(graph,'file.dot')
