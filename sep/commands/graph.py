# coding:utf-8
import io
import networkx
import os
import matplotlib.pyplot as plt

import nltk
from sep import context
from sep import ranking

def load():
    ranks = ranking.loadnnranking()
    words = set(w[0] for w in ranks)
    dbdir = context.dbdir()
    edges = []
    cache = set()
    with io.open(os.path.join(dbdir,'cooccurence.csv')) as fio:
        for line in fio:
            word0,word1,count = line.rstrip().split("\t")
            key0,key1 = sorted((word0,word1))
            key = (key0,key1)
            if key in cache: continue
            cache.add(key)
            if word0 in words and word1 in words:
                edges.append((word0,word1,int(count)))

    edges.sort(lambda x,y:cmp(y[2],x[2]))
    return edges[:30]

def loadgraph():
    edges = load()
    graph = networkx.Graph()
    for word0,word1,weight in edges:
        graph.add_edge(word0,word1,weight=weight)

    return graph
    
def graphdraw():
    graph = loadgraph()
    networkx.draw(graph)
    #pos = networkx.spring_layout(graph)
    #networkx.draw_networkx_nodes(graph, pos, node_size = 100, node_color = 'w')
    #networkx.draw_networkx_edges(graph, pos, width = 1)
    #networkx.draw_networkx_labels(graph, pos, font_size = 12, font_family = 'sans-serif', font_color = 'r')
    #plt.xticks([])
    #plt.yticks([])
    plt.savefig('graph.png')
