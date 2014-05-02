# coding:utf-8
import os
import io
import nltk

HOMEDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
DATADIR = os.path.join(HOMEDIR, 'data')
HTMLDIR=os.path.join(HOMEDIR, "data","html")
TEXTDATADIR=os.path.join(HOMEDIR, "data", "text")
DBDIR = os.path.join(HOMEDIR, "data", "db")
GRAPHDIR = os.path.join(HOMEDIR, "data", "graph")

class Context():
    def textdatadir(self):
        return textdatadir()

def datadir():
    return DATADIR

def graphdir():
    return GRAPHDIR

def dbdir():
    return DBDIR

def textdatadir():
    return TEXTDATADIR

def htmldir():
    return HTMLDIR

def url2filename(link):
    filename = link.split('/')[-2] + '.html'
    return filename

def url2path(link):
    filename = url2filename(link)
    return os.path.join(SAVEDIR, filename)

def filenames():
    textdir = textdatadir()
    files = []
    for fpath in os.listdir(textdir):
        fullpath = os.path.join(textdir, fpath)
        if os.path.isfile(fullpath):
            files.append(fullpath)

    return files
    
def articles():
    textdir = textdatadir()
    texts = []
    for fpath in os.listdir(textdir):
        fullpath = os.path.join(textdir, fpath)
        if os.path.isfile(fullpath):
            yield readarticle(fullpath)

def readarticle(filepath):
    with open(filepath) as fio:
        string = fio.read()
        return string

