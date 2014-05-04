# coding:utf-8

u"""
normalize author names.

ex.::

D. Lewis -> David Lewis
W.V. Quine -> W.V.O. Quine
K L Walton -> Kendal L. Walton
"""
from collections import Counter
from collections import defaultdict
from sep.lib import index
import re

def isshortname(shortname, name):
    if not shortname or not name: return False
    if len(shortname)==1 and name[0].upper() == shortname and len(name)>1:
        # ex. D and David
        return True
    elif isinitial(shortname) and name[0] == shortname[0]:
        # ex. D. and David
        return True
    elif len(shortname) < len(name) and name.startswith(shortname):
        # ex. W.V. and W.V.O.
        return True
    elif isinitials(shortname):
        inis = filter(lambda x:x,shortname.split('.'))
        names = name.split(' ')
        return len(names)==len(inis) and all([isshortname(ini,namep) for ini, namep in zip(inis,names)])
    else:
        return False

def isinitial(str0):
    return len(str0)==2 and 'A' <= str0[0] <= 'Z' and str0[1]=='.'
iniseqreg = re.compile("^([A-Z]\.){2,}$")
def isinitials(str0):
    return bool(re.match(iniseqreg, str0))

def issamename(str0, str1):
    return isshortname(str0, str1) or isshortname(str1, str0) or str0 == str1

class MiddleNames(object):
    def __init__(self):
        self.dic = defaultdict(dict)
    def add(self, firstname, lastname, middlename):
        if not middlename:return
        middlename = middlename.rstrip().lstrip()
        if not middlename:return
        if len(middlename)==1: middlename += '.'
        key = firstname
        val = middlename
        # firstname -> use first regstered item
        # middlename -> use longest name
        for firstname2, middlename2 in self.dic[lastname].iteritems():
            if issamename(firstname2, firstname):
                key = firstname2
                if isshortname(middlename, middlename2):
                    val = middlename2

                break

        self.dic[lastname][key] = val
    def get(self, firstname, lastname, middlename=None):
        for firstname2, othermiddlename in self.dic[lastname].iteritems():
            # search same firstname
            if issamename(firstname2, firstname):
                if not middlename or isshortname(middlename, othermiddlename):
                    return othermiddlename

        return middlename

class NameIndex(object):
    def __init__(self):
        self.dic = {}
        self.counter = Counter()
        self.longnames = defaultdict(Counter)
    def add(self, name):
        self.counter[name] += 1
        if len(name) > 2:
            ini = name[0] + '.'
            self.longnames[ini][name] += 1
            self.dic[ini] = self.longnames[ini].most_common()[0][0]

    def get(self, name):
        if len(name)==1: name += '.'
        return self.dic.get(name, name)

class AuthorName(object):
    def __init__(self, firstname, lastname, middlename=None):
        self.firstname = firstname
        self.lastname = lastname
        self.middlename = middlename

    def __str__(self):
        if self.middlename:
            if isinitial(self.firstname):
                return u"%s%s %s" % (self.firstname, self.middlename, self.lastname)
            else:
                return u"%s %s %s" % (self.firstname, self.middlename, self.lastname)
        else:
            return u"%s %s" % (self.firstname, self.lastname)

    splitreg = re.compile("and|,")
    @classmethod
    def parse(cls, name):
        names = name.split(' ')
        if 'and' in names:
            names = re.split(cls.splitreg, name)
            authornames = []
            for name in names:
                authornames.append(cls.parse(name.strip()))

            return AuthorNames(authornames)

        firstname = names[0]
        lastname = names[-1]
        middlename = None
        if '.' in firstname:
            inis = firstname.split('.')
            firstname = inis[0]
            if len(inis[0])==1:
                firstname += '.'

            middlename = ".".join(inis[1:])

        if 1==len(firstname):
            firstname += '.'
        if len(names)>=3:
            if middlename:
                middlename = " ".join([middlename] + names[1:-1])
            else:
                middlename = " ".join(names[1:-1])

        return cls(firstname=firstname, lastname=lastname, middlename=middlename)

class AuthorNames(AuthorName):
    def __init__(self, names):
        self.names = names
    def __iter__(self):
        return iter(self.names)
    def __str__(self):
        names = self.names
        ret = unicode(names[0])
        for i, name in enumerate(self.names[1:]):
            if i == len(self.names)-2:
                ret += " and "
            else:
                ret += ", "

            ret += unicode(name)

        return ret
class Authors(object):
    def __init__(self):
        self.authordict = {}
        self.firstnames = defaultdict(NameIndex)
        self.middlenames = MiddleNames()
    def add(self, author):
        if not author: return
        name = AuthorName.parse(author)
        if isinstance(name, AuthorNames):
            names = name
        else:
            names = [name]

        for name in names:
            firstname = name.firstname
            lastname  = name.lastname
            self.firstnames[lastname].add(firstname)
            self.middlenames.add(firstname, lastname, name.middlename)

    def normalize(self, author):
        name = AuthorName.parse(author)
        if isinstance(name, AuthorNames):
            names = name
        else:
            names = [name]

        newnames = []
        for name in names:
            newfirstname = self.firstnames[name.lastname].get(name.firstname)
            middlename   = self.middlenames.get(firstname=name.firstname, lastname=name.lastname, middlename=name.middlename)
            newname = AuthorName(firstname=newfirstname, middlename=middlename, lastname=name.lastname)
            newnames.append(newname)

        newname = AuthorNames(newnames)
        return unicode(newname)
