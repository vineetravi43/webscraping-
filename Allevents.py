# -*- coding: utf-8 -*-
import scrapy

class Allevents(scrapy.Spider):
    name = 'allevents'
    allowed_domains = ['allevents.in']
    start_urls = (
        'https://allevents.in/new%20delhi/all#',
    )

    def parse(self, response):

        urls = response.xpath('//h3[@class="name"]/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_event)
            yield request

        next_page_url = response.xpath('//a[text()="Next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_event(self, response):
        name = response.xpath(
        '//*[@id="event-container"]/@data-title').extract_first()
        time= response.xpath('//*[@id="event-container"]/@data-Time').extract_first()
        place=response.xpath('//*[@id="event-container"]/@data-Venue').extract_first()

        event = {
            'name': name,
            'time':time,
            'place':place,
            'url': response.url}
        yield event
