import scrapy
from urllib.parse import urljoin
import pandas as pd

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        all_books = response.xpath('//article[@class="product_pod"]')
        for book in all_books:
            book_url = self.start_urls[0] + book.xpath('.//h3/a/@href').extract_first()

            yield scrapy.Request(book_url,callback = self.parse_book) # self-defined method

    def parse_book(self,response):
        title = response.xpath('//div/h1/text()').extract_first()

        relative_img_path = response.xpath('//div[@class="item active"]/img/@src').extract_first()
        full_img_path = urljoin(self.start_urls[0],relative_img_path)

        price = response.xpath('//div[contains(@class,"product_main")]/p[@class="price_color"]/text()').extract_first()
        # Quite Tricky
        stars = response.xpath('//div/p[contains(@class,"star-rating")]/@class').extract_first().replace("star-rating","")
        # Description with out a class attribute => use following-sibling
        des  = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').extract_first()

        # HTML Table Use Pandas
        df = pd.read_html(response.url)[0]
        df.columns = ["P-Info-Title","P-Info-Details"]
        upc = df['P-Info-Details'][0]
        price_inc_tax =df['P-Info-Details'][3]
        instock = df['P-Info-Details'][5]

        # Output
        item = {
                'title':title,
                'upc':upc,
                'img':full_img_path,
                'stars':stars,
                'des':des,
                'price':price,
                'price_inc_tax':price_inc_tax,
                'instock':instock,
        }
        yield item
