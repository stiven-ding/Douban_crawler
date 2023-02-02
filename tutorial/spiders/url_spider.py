import scrapy
from furl import furl
from datetime import date
import json


def stringToDict (cookie):
    itemDict = {}
    items = cookie.split(';')
    for item in items:
        if item == '':
            continue
        key = item.split('=')[0].replace(' ','')
        value = item.split ('=') [1]
        itemDict [key] = value
    return itemDict


class UrlSpider(scrapy.Spider):
    name = "url_spider"

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 3,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.2,
        'LOG_LEVEL': 'INFO'
    }

    def start_requests(self):
        url_db_file = open('./url/movie_list.json', 'r')
        url_db_json = json.load(url_db_file)

        cookies_string = 'bid=QVMqdux_yng; __utmz=30149280.1675240183.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="118231"; __utma=30149280.1313131172.1675240183.1675240183.1675242740.2; ap_v=0,6.0; ck=AFY0; push_noty_num=0; push_doumail_num=0; _pk_id.100001.8cb4=9a5a279f14f0e179.1675247517.2.1675305541.1675247517.; _pk_ses.100001.8cb4=*'
        cookies = stringToDict(cookies_string)

        i = 0
        for item in url_db_json:
            if i > 107:
                yield scrapy.Request(url=item['search_url'], callback=self.parse, cookies=cookies,
                meta={'title': item['title'], 'index': i, 'total': len(url_db_json), 'playwright': True})
            i = i + 1

    def parse(self, response):
        
        if len(response.css('div.item-root')) == 0:
            print("No result for " + response.meta['title'])

            yield {
                'index': response.meta['index'],
                'total': response.meta['total'],
                'movie_id': 'NA',
                'title': response.meta['title'], 
                'url': 'NA',
            }

        else: 
            item = response.css('div.item-root')[0]

            yield {
                'index': response.meta['index'],
                'total': response.meta['total'],
                'movie_id': item.css("a::attr(href)").get().split('/')[4],
                'title': response.meta['title'], 
                'url': item.css("a::attr(href)").get(),
            }

        print(str(response.meta['index']) + " / " + str(response.meta['total']))

 