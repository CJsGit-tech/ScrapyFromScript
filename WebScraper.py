from Spiders.MultiSpider import BookSpider
from Spiders.SingleSpider import SpiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

allowed_domains = ['books.toscrape.com']
start_urls = ['http://books.toscrape.com/']

rules = [
        Rule(LinkExtractor(allow='catalogue/'),
        callback = 'parse_filter_book',follow = True
        )
]

# Configure Settings
# https://docs.scrapy.org/en/latest/topics/settings.html
file_name = "Books_Details_Scraper"
program = CrawlerProcess(settings={
        'LOG_FILE':'log.txt',
        'LOG_LEVEL':'INFO',
        'FEEDS':{
            f'{file_name}.json':{
                    'format':'json',
                    'overwrite':True
            }
        },
        'FEED_EXPORT_ENCODING':'utf-8', # In case you are scraping a non-English Website
        'AUTOTHROTTLR_ENABLED':True, # To reduce target server's burden and avoid DoS
        'DOWNLOADER_MIDDLEWARES':{
        'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': True,

        }
})


# Run By Script
# Initialize Your Spider
program.crawl(SpiderSpider,allowed_domains=allowed_domains,start_urls = start_urls,rules = rules)
# Execute
program.start()
