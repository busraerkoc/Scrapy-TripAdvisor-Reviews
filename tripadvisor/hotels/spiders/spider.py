# -*- coding: utf-8 -*-
import scrapy
from hotels.items import HotelsItem
from urllib.parse import urljoin
import re

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    #alowed_domains = ['https://www.tripadvisor.com/Hotels-g191-United_States-Hotels.html']
    start_urls = ['https://www.tripadvisor.co.uk/Hotel_Review-g187791-d229101-Reviews-Colonna_Palace_Hotel-Rome_Lazio.html']

    def parse(self, response):
        for href in response.xpath('//div[contains(@class,"reviewTitle")]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_review)

        url = "https://www.tripadvisor.co.uk/Hotel_Review-g187791-d229101-Reviews-Colonna_Palace_Hotel-Rome_Lazio.html"
        
        for i in range(51):
            if not re.findall(r'or\d', url):
                next_page = re.sub(r'(-Reviews-)', r'\g<1>or5-', url)
                pagenum = 5
                url = next_page
            else:
                pagenum = int(re.findall(r'or(\d+)-', url)[0])
                pagenum_next = pagenum + 5
                next_page = url.replace('or' + str(pagenum), 'or' + str(pagenum_next))
                url = next_page
            yield scrapy.Request(next_page,meta={'dont_redirect': True},callback=self.parse)
        

    def parse_review(self, response):
        item = HotelsItem()
        item['country'] = "Italy"
        item['city'] = 'Rome'
        item['titleHotel'] = response.xpath('//a[@class="ui_header h2"]/text()').extract()
        item['title'] = response.xpath('//div[@class="quote"]/h1/text()').extract()[0][0:]  # strip the quotes
        item['content'] = response.xpath('//div[@class="entry"]/p/span/text()').extract()[0]
        item['rating'] = response.xpath('//span[contains(@class,"ui_bubble_rating")]/@class').extract()[0][-2:-1]
        
        #item['stars'] = response.xpath('//span[starts-with(@class, "rating")]/span/@alt').extract()[0].replace('bubble', 'star')
        return item