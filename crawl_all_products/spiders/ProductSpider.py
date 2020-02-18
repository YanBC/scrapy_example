# -*- coding: utf-8 -*-
import scrapy
from crawl_all_products.items import Product


class ProductSpider(scrapy.Spider):
    name = 'ProductSpider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/index.html']

    def parse(self, response):
        for product_container in response.css('article.product_pod'):
            product_url = product_container.css('div.image_container a::attr(href)').get()
            if product_url is not None:
                product_url = response.urljoin(product_url)
                yield scrapy.Request(product_url, callback=self.parse_product)

        next_page = response.css('li.next a::attr(href)').get()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


    def parse_product(self, response):
        name = response.css('div.product_main h1::text').get()
        image_urls = response.css('img::attr(src)').get()
        image_urls = [response.urljoin(image_urls)]
        price = response.css('p.price_color::text').get()

        table = response.css('table.table tr')
        for tr in table:
            if tr.css('th::text').get() == 'UPC':
                upc = tr.css('td::text').get()
                break
        else:
            upc = None

        yield Product(name=name, image_urls=image_urls, price=price, upc=upc)

