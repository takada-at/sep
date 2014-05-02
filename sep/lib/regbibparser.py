# coding:utf-8
import re

shortname = re.compile(u'^\[([^\]]+)\] ')
forthcoming = re.compile(u'(unpublished|forthcoming)')
year = re.compile(u'\(?([0-9]{4,4})\)?\.?')
#book = re.compile(u'(?:<em>|<i>)([^<]+)(?:</em>|</i>)')
book = re.compile(u'(?:<em>|<i>)(.+?)(?:</em>|</i>)')
paper = re.compile(u'(?:“|‘)(.+),?\.?(?:”|’)')

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
    for item in items:
        parsed = parseitem(item)
        if not parsed:
            print item
            print 'unknown format: %s' % item
            continue

        if prev and '–––' in parsed.get('author', ''):
            parsed['author'] = parsed['author'].replace('–––', prev['author'])

        prev = parsed
        key = (parsed.get('author', ''), parsed.get('year'), parsed.get('title'))
        if key in cache: continue
        cache.add(key)
        res.append(parsed)

    return res
    
def parseitem(item):
    item = item.replace('<li>','').replace('</li>', '')
    result = parseshortname(item)
    if result:
        return result

    prev0, yearval, rest0 = parseyear(item)
    if yearval is None:
        print 'not year',item
        yearval = ''

    #pattern: author -> book title -> year
    if '<em>' in prev0 or '':
        prev1, title, rest1, itype = fetchtitle(prev0)
        author = parseauthor(prev1)
    else:
        author = parseauthor(prev0)
        prev1, title, rest1, itype = fetchtitle(item)

    if title:
        return itype(author=author, title=title, year=yearval, raw=item)

    prev1,title,rest1,itype = fetchtitle(rest0, force=True)
    return Book(author=author, title=title, year=yearval, raw=item)

def parseshortname(item):
    reg = shortname
    m = re.search(reg, item)
    if m:
        items = re.split(reg, item)
        tag = items[1]
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

def parseauthor(item):
    if item is None:
        return ''

    nameparts = [p.rstrip() for p in item.split(', ') if p]
    if len(nameparts)==0:
        return ''

    if len(nameparts)==1:
        return nameparts[0]

    author = " ".join(nameparts[1:] + [nameparts[0]])
    if '(ed.)' in author:
        author = author.replace(' (ed.)', '')
        author += ' (ed.)'

    if author == u'–––.':
        author = u'–––'

    return author

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
