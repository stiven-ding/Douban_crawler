import scrapy
from furl import furl
from datetime import date
import json

class RatingSpider(scrapy.Spider):
    name = "rating_spider"

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': False,
        'AUTOTHROTTLE_START_DELAY': 0.2,
        'AUTOTHROTTLE_MAX_DELAY': 5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.7,
        'LOG_LEVEL': 'INFO'
    }

    def start_requests(self):
        url_db_file = open('./url/url_db.json', 'r')
        url_db_json = json.load(url_db_file)

        for item in url_db_json:
            yield scrapy.Request(url=item['url'], callback=self.parse, meta={
                'id': item['id'],
                'catagory': item['catagory'],
                'location': item['location'],
                'date_url_discovered': item['date_url_discovered'],
                "playwright": True
            })

    def parse(self, response):
        cname = response.meta['catagory']

        for item in response.css('div.grid-item'):
            yield {
                'id': item.css("a::attr(aria-labelledby)").get(),
                'url': item.css("a::attr(href)").get(),
                'title': item.css("div.fund-title.show-for-medium::text").get(), 
                'image': item.css("div.campaign-tile-img--contain::attr(data-original)").get(),
                'catagory': cname,
                'location': item.css("div.fund-location").css("span::text").get(),
                'date_url_discovered': date.today().strftime("%Y-%m-%d"),
            }

 