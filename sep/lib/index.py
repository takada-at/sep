# coding:utf-8

class Index(object):
    def __init__(self):
        self.dic = {}
    def add(self, key):
        keylen = len(key)
        subkeys = [key[:i] for i in range(1,len(key)+1)]
        for subkey in subkeys:
            entry = self.dic.get(subkey, '')
            if len(entry) < len(key): self.dic[subkey] = key
    def search(self, key):
        subkeys = [key[:i] for i in range(1,len(key)+1)]
        subkeys.reverse()
        for subkey in subkeys:
            if subkey in self.dic:
                return self.dic.get(subkey)
