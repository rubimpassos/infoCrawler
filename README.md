Info Rss Crawler - Export rss feed as json
===============================================

InfoCrawler is a proposal of solution to the infoGlobo back-end challenge at https://github.com/Infoglobo/desafio-back-end

Requeriments
----------------------

* Python 3.6
* BeautifulSoup 4
* requests
* mock


How to use
----------------------

You can use as CLI
    
    python -m infocrawler "https://revistaautoesporte.globo.com/rss/ultimas/feed.xml" -f "feed.json"

Or API

    from infocrawler.crawler import feed_reader
    
    json_string = feed_reader("https://revistaautoesporte.globo.com/rss/ultimas/feed.xml")