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
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.3,
        'LOG_LEVEL': 'INFO'
    }

    def start_requests(self):
        url_db_file = open('./url/movie_list.json', 'r')
        url_db_json = json.load(url_db_file)

        cookies_string = 'bid=QVMqdux_yng; __utmz=30149280.1675240183.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="118231"; __utma=30149280.1313131172.1675240183.1675240183.1675242740.2; ap_v=0,6.0; ck=AFY0; push_noty_num=0; push_doumail_num=0; _pk_id.100001.8cb4=9a5a279f14f0e179.1675247517.2.1675305541.1675247517.; _pk_ses.100001.8cb4=*'
        cookies = stringToDict(cookies_string)

        i = 0
        for item in url_db_json:
            if i > -1:
                yield scrapy.Request(url=item['movie_url'], callback=self.parse, cookies=cookies,
                meta={'movie_id': item['movie_id'], 'title': item['title'], 'movie_url': item['movie_url'], 'index': i, 'total': len(url_db_json), 'playwright': True})
            i = i + 1

    def parse(self, response):
        
        if len(response.css('div.item-root')) == 0:
            print("No result for " + response.meta['title'])

            yield {
                'movie_id': response.meta['movie_id'],
                'title': response.meta['title'], 
                'url': response.meta['movie_url']
            }

        else: 
            item = response.css('div.item-root')[0]

            yield {
                'movie_id': response.meta['movie_id'],
                'title': response.meta['title'], 
                'url': response.meta['movie_url']
            }

        print(str(response.meta['index']) + " / " + str(response.meta['total']))

 