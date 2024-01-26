

import scrapy
from pymongo import MongoClient

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    def __init__(self, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.client = MongoClient('localhost', 27017)  # Assurez-vous de remplacer cela par vos paramètres MongoDB
        self.db = self.client['quotes_database']

    def closed(self, reason):
        self.client.close()

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()

            # Stocker dans MongoDB
            self.db.quotes.insert_one({
                'text': text,
                'author': author,
            })

            yield {
                'text': text,
                'author': author,
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
