# Scrapy settings for sep project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sep'

SPIDER_MODULES = ['sep.spiders']
NEWSPIDER_MODULE = 'sep.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sep (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 3

ITEM_PIPELINES = {
    'sep.pipelines.SavePipeline': 100,
    'sep.pipelines.ConvertPipeline': 200,
}
