# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import io
import sep.util as util
from sep.items import Html
import sep.convert

class SavePipeline(object):
    def process_item(self, item, spider):
        fpath = util.url2path(item['link'])
        with io.open(fpath, 'w', encoding='utf_8') as wio:
            content = item['content']
            wio.write(content)

        return Html(filepath=fpath)

class ConvertPipeline(object):
    def process_item(self, item, spider):
        sep.convert.handlefile(item['filepath'])
