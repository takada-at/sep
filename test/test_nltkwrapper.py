# coding:utf-8

import prepare
prepare

from mock import Mock
import nltk
from sep import context
from sep import nltkwrapper
from sep.nltkwrapper import Stem
from sep.nltkwrapper import Vocab
def dummy_articles():
    string = u'''Hello I am John.
You have sisters. John paid money.
It's Wonderful day.
'''
    yield string

def dummy_reader():
    article = dummy_articles().next()
    reader = Mock()
    nltkwrapper.PlaintextCorpusReader = Mock(return_value=reader)
    reader.words.return_value = nltk.wordpunct_tokenize(article)
    reader.sents.return_value = [nltk.wordpunct_tokenize(article) for sent in nltk.sent_tokenize(article)]
def test_Vocab():
    dummy_reader()
    vocab = Vocab(context)
    words = vocab.vocab()
    assert words is not None
    words = dict(words).keys()
    simdict = vocab.cooccurence(words)
    assert simdict is not None
    assert simdict[('money', 'paid')] > 0
def test_Stem():
    dummy_reader()
    stemmer = Stem()
    stem0 = stemmer.stem('worldly')
    assert 'worldli' == stem0
    assert 'worldly' == stemmer.orgword('worldli')
    stem1 = stemmer.stem('natur')
    assert 'nature' == stemmer.orgword('natur')
