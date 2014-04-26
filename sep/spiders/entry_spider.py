# coding:utf-8
import os
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from sep.items import EntryItem
import sep.util as util

def clean(content):
    return content.replace("\n","")

class EntrySpider(Spider):
    name = "entry"
    allowed_domains = ["plato.stanford.edu"]
    start_urls = [
        "http://plato.stanford.edu/contents.html",
    ]

    def parse_entry(self, response):
        hxs = Selector(response)
        link = response.url
        title = link
        #title = hxs.xpath("//h1/text()").extract()[0]
        content = response.body.decode('utf-8')
        yield EntryItem(title=title, content=content, link=link)
    def parse(self, response):
        entriespath = "//div[@id='content']/*/li/a[contains(@href,'entries/')]"
        hxs = Selector(response)
        entries = hxs.xpath(entriespath)
        urls = []
        for entry in entries:
            #title = entry.xpath("strong/text()").extract()[0]
            link  = entry.xpath("@href").extract()[0]
            url   = "http://plato.stanford.edu/" + link
            urls.append(url)

        urls.sort()
        for url in urls:
            filepath = util.url2path(url)
            if os.path.exists(filepath):
                continue
                
            req = Request(url, callback=self.parse_entry)
            yield req

