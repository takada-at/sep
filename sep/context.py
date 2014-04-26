# coding:utf-8
import os
import io
from sep import nltkwrapper
import nltk

HOMEDIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
SAVEDIR=os.path.join(HOMEDIR, "save")
TEXTDATADIR=os.path.join(HOMEDIR, "text")
DBDIR = os.path.join(HOMEDIR, "db")


class Context():
    def load(self):
        self.texts, self.rawtexts, self.collections = createcollection()

def dbdir():
    return DBDIR

def textdatadir():
    return TEXTDATADIR
    
def dirname():
    return SAVEDIR
    
def url2filename(link):
    filename = link.split('/')[-2] + '.html'
    return filename

def url2path(link):
    filename = url2filename(link)
    return os.path.join(SAVEDIR, filename)

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

def createcollection():
    texts = []
    rawtexts = []
    for string in articles():
        rawtexts.append(string)
        text = nltkwrapper.createtext(string)
        texts.append(text)

    collection = nltk.text.TextCollection(texts)
    return (texts, rawtexts, collection)

