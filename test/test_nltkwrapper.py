# coding:utf-8

import prepare
prepare

from sep import context
from sep.nltkwrapper import Vocab
def dummy_articles():
    string = u'''Hello I am John.
You have sisters. John paid money.
It's Wonderful day.
'''
    yield string
def test_Vocab():
    context.articles = dummy_articles
    ctx = context.Context()
    vocab = Vocab(ctx)
    words = vocab.vocab()
    assert words is not None
    words = dict(words).keys()
    simdict = vocab.cooccurence(words)
    assert simdict is not None
    assert simdict[('money', 'paid')] > 0
