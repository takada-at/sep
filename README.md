# sep processing

Scraping and Natural Language Processing for Stanford Encyclopedia of Philosophy.


Install
```
git clone https://github.com/takada-at/sep.git
cd sep/
pip install -r requirements.txt
```

Usage
```
python bin/sepgen.py prepare
scrapy crawl entry
python bin/sepgen.py coocurence
python bin/sepgen.py graph
```