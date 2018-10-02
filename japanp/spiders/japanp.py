# -*- coding: utf-8 -*-
import scrapy
import re
import time

class JapanpSpider(scrapy.Spider):
    name = 'japanp'
    allowed_domains = ['japan-partner.com']
    login_url = 'https://www.japan-partner.com/user.php'
    start_urls = ['https://www.japan-partner.com/car-auction-old/list.html?p=1&a=5,18,19,20,179,21,22,23,49,4,228,9,10,11,14,39,41,45,47,51,52,66,67,68,71,69,70,73,74,77,81,79,82,84,88,91,92,93,94,106,112,6,7,8,12,17,24,27,28,36,37,53,54,187,59,213,72,75,86,97,100,103,108,110,231,2,13,16,26,29,32,34,35,38,50,55,57,60,62,76,80,78,83,85,87,89,90,95,111,113,1,25,30,31,40,43,44,46,48,56,58,64,99,102,105,107,3,15,33,42,184,61,63,65,96,98,101,104,109&mk=&md=&ys=2015&ye=&ds=&de=&ms=&me=&ps=&pe=&gr=&t=&tr=&r=&ls=&le=&l=0&ta=&m=3m&withPrices=0']
    count = 1
    def start_requests(self):
        data = {
            'a': 'login',
            'referer': '/',
            'savepass': 'yes',
            'send': 'yes',
            'login': 'majidbilaly@gmail.com',
            'pass': 'asdf1234',
        }
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.logged_in)


    def logged_in(self, response):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        #yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
        #next_page_url = response.css('a#nextPage').extract_first()
        urls = response.css('nobr > a::attr(href)').extract()
        next_page_url = response.urljoin(response.css('a#nextPage::attr(href)').extract_first())

        for url in urls[:]:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)

        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        tds = response.css('table.mainStockTable > tr > td')
        #tds = response.css('table.mainStockTable > tr > td')
        #tds = trs.xpath('.//td')
        yield {
            'Date': re.sub(r'[\n\t]', "", ' '.join(tds[0].xpath('.//text()').extract())),
            'Lot No.': re.sub(r'\D', "", ' '.join(tds[1].xpath('.//text()').extract())),
            'Make': re.sub(r'[\n\t]', "", ' '.join(tds[2].xpath('.//text()').extract())),
            'Price Details': re.sub(r'[\n\t]', "", ' '.join(tds[3].xpath('.//text()').extract())),
            'Vehicle Details1': re.sub(r'[\n\t]', "", ' '.join(tds[4].xpath('.//text()').extract())),
            'Vehicle Details2': re.sub(r'[\n\t]', "", ' '.join(tds[5].xpath('.//text()').extract())),
            'Rating': re.sub(r'[\n\t]', "", ' '.join(tds[6].xpath('.//text()').extract()))
        }
        time.sleep(5)
