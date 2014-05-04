# coding:utf-8
import logging
import re
from sep.lib.authors import Authors
shortname = re.compile(u'^\[([^\]]+)\] ')
forthcoming = re.compile(u'\(?(unpublished|forthcoming)\)?\.?')
year = re.compile(u'\[?\(?([0-9]{4})\)?\]?\.?')
#book = re.compile(u'(?:<em>|<i>)([^<]+)(?:</em>|</i>)')
book = re.compile(u'(?:<em>|<i>)(.+?)(?:</em>|</i>)')
paper = re.compile(u'(?:“|‘)(.+),?\.?(?:”|’)')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class BibItem(dict):
    pass
class Paper(BibItem):
    def type(self):
        return 'paper'
class Book(BibItem):
    def type(self):
        return 'book'

def parseitems(items):
    res = []
    prev = None
    cache = set()
    authors = Authors()
    for item in items:
        parsed = parseitem(item)
        if not parsed:
            #logger.info('unknown format: %s' % item)
            continue

        if 'author' not in parsed: parsed['author'] = ''
        if prev and '–––' in parsed.get('author', ''):
            parsed['author'] = parsed['author'].replace('–––', prev['author'])

        prev = parsed
        # avoid double entry
        #key = (parsed.get('author', ''), parsed.get('year'), parsed.get('title'))
        #if key in cache: continue
        #cache.add(key)

        authors.add(parsed.get('author'))
        res.append(parsed)

    # normalize author name
    for item in res:
        if '[' in item['author']: print item['raw'],item['author']
        item['author'] = authors.normalize(item['author'])

    return res
    
def parseitem(item):
    item = item.replace('<li>','').replace('</li>', '')
    result = parseshortname(item)
    if result:
        return None

    prev0, yearval, rest0 = parseyear(item)
    if not yearval:
        return None

    #pattern: author -> book title -> year
    if '<em>' in prev0 or '':
        prev1, title, rest1, itype = fetchtitle(prev0)
        author = parseauthor(prev1)
    else:
        author = parseauthor(prev0)
        prev1, title, rest1, itype = fetchtitle(item)

    if not author: return
    if title:
        return itype(author=author, title=title, year=yearval, raw=item)

    prev1,title,rest1,itype = fetchtitle(rest0, force=True)
    return Book(author=author, title=title, year=yearval, raw=item)

def parseshortname(item):
    reg = shortname
    m = re.search(reg, item)
    if m:
        items = re.split(reg, item)
        prev,title,rest,itype = fetchtitle(items[2])
        return Book(title=title, raw=item)
    else:
        return None

def parseyear(item):
    reg = year
    m = re.search(reg, item)
    if m:
        yearval = int(m.group(1))
        items = re.split(reg, item)
        return (items[0], yearval, "".join(items[1:]))
    m = re.search(forthcoming, item)
    if m:
        yearval = m.group(1)
        items = re.split(reg, item)
        return (items[0], yearval, "".join(items[1:]))

    items = item.split(',')
    return (items[0], '', "".join(items[1:]))

commentreg = re.compile(' \[.*?\]')
splitreg = re.compile(', | and |&amp;')
def parseauthor(item):
    if item is None:
        return ''

    # remove comment such as 'Barnes, J. [O. Testudo, pseud.],'
    item = re.sub(commentreg, '', item)
    item = item.replace('[','').replace(']','')
    if '(' in item and ')' not in item:
        return ''

    nameparts = [_normalizepart(p.strip()) for p in re.split(splitreg, item) if p]
    if len(nameparts)==0:
        return ''

    if len(nameparts)==1:
        return _normalizefullname(nameparts[0])

    # ex. Quine, W.V.O
    # ex. Lewis, David, and Gideon Rosen
    # ex. Lewis, D. and S. Lewis
    # ex. Hardy, J. D., H. J. Wolff and H. Goodell
    lastname = nameparts[0]
    nameparts = nameparts[1:]
    nameparts[0] += " " + lastname
    author = nameparts[0]
    for i in range(1, len(nameparts)):
        if not nameparts[i]: continue
        cname = normalizefirstname(nameparts[i])
        if i == len(nameparts)-1:
            author += ' and ' + cname
        else:
            author += ', ' + cname

    if '(ed.)' in author or ' ed. ' in author:
        author = author.replace(' (ed.)', '').replace(' ed.', '')
        author += ' (ed.)'

    return _normalizefullname(author)

def _normalizepart(part):
    if part.startswith('and '):
        part = part[4:]

    return part

def _normalizefullname(author):
    author = _sharpendot(author)
    while len(author) and author[-1] == '.':
        author = author[:-1]

    return author
def normalizefirstname(firstname):
    if not firstname: return firstname
    if len(firstname)==1 and "A" < firstname < "Z":
        firstname += "."
    elif len(firstname) > 2 and firstname[-1] == '.' and '.' not in firstname[:-1]:
        firstname = firstname[:-1]
    elif firstname[-1] == ',':
        firstname = firstname[:-1]

    while firstname.endswith('..'):
        firstname = firstname[:-1]

    return firstname

reginitials = re.compile(u"(?:([A-Z]\.) ){2,}")
def _sharpendot(name):
    u"""
    convert: W. V. O. Quine -> W.V.O. Quine
    """
    m = re.search(reginitials, name)
    if m:
        # ex. W. V. O. 
        ini = m.group(0)
        # ex. W.V.O.
        iniconverted = ini.replace(". ", ".") + " "
        return name.replace(ini, iniconverted)

    return name
    
def fetchtitle(item, force=False):
    prev, title, rest = parsepaper(item)
    if title:
        return (prev,title,rest, Paper)

    prev,title,rest = parsebook(item)
    if title:
        return (prev,title,rest, Book)

    if force:
        return (None,item.split(',')[0],None,Book)

    return (None,None,None,Book)
    
def parsepaper(item):
    reg = paper
    m = re.search(reg, item)
    if m:
        title = m.group(1)
        if title[-1] in '.,':
            title = title[:-1]

        items = re.split(reg, item)
        return (items[0], title, "".join(items[1:]))

    return (None,None,None)

def parsebook(item):
    reg = book
    m = re.search(reg, item)
    if m:
        title = m.group(1)
        items = re.split(reg, item)
        return (items[0], title, "".join(items[1:]))

    return (None,None,None)
