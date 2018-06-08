Info Crawler - Export rss feed as json
===============================================

InfoCrawler is a proposal of solution to the infoGlobo back-end challenge at https://github.com/Infoglobo/desafio-back-end
Fully tested and extendable, easy to use in any project

Requeriments
----------------------

* Python 3.6
* BeautifulSoup 4
* requests
* mock

How to Install and Use
----------------------

Download the project zip
 
 [InfoCrawler](https://github.com/rubimpassos/infoCrawler/archive/master.zip)

Install Python 3.6 or greater and run

    pip install -r infoCrawler/requirements.txt

You can use as CLI
    
    python -m infocrawler "https://revistaautoesporte.globo.com/rss/ultimas/feed.xml" -f "feed.json"

Or as API

    from infocrawler.crawler import feed_reader
    
    json_string = feed_reader("https://revistaautoesporte.globo.com/rss/ultimas/feed.xml")