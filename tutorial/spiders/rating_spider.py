import time
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

class RatingSpider(scrapy.Spider):
    name = "rating_spider"
    
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 4,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.15,
        'LOG_LEVEL': 'INFO',
        'COOKIES_ENABLED' : True
    }

    def start_requests(self):
        url_db_file = open('./url/movie_list.json', 'r')
        url_db_json = json.load(url_db_file)

        cookies_string = 'bid=QVMqdux_yng; __utmz=30149280.1675240183.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ll="118231"; __utma=30149280.1313131172.1675240183.1675240183.1675242740.2; ap_v=0,6.0; ck=AFY0; push_noty_num=0; push_doumail_num=0; _pk_id.100001.8cb4=9a5a279f14f0e179.1675247517.2.1675305541.1675247517.; _pk_ses.100001.8cb4=*'
        cookies = stringToDict(cookies_string)

        i = 0
        for item in url_db_json:
            if i > 26:
                if i % 20 == 19:
                    print("Sleeping...")
                    time.sleep(10)
                yield scrapy.Request(url=item['movie_url'], callback=self.parse, #cookies=cookies,
                meta={'movie_id': item['movie_id'], 'movie_url': item['movie_url'], 'title': item['title'], 'index': i, 'total': len(url_db_json),
                'playwright': True, "playwright_context": "persistent"})
            i = i + 1

    def parse(self, response):
        rating_num = response.css('strong.rating_num::text')

        # douban rating not available
        if 'sec.douban.com' in response.request.url:
            print("403 " + response.meta['title'])

            yield {
                'movie_id': response.meta['movie_id'],
                'title': response.meta['title'], 
                'url': response.request.url,
                'rating_overall': 'ERR',
                'rating_num': 'ERR',
                'rating_5': 'ERR',
                'rating_4': 'ERR',
                'rating_3': 'ERR',
                'rating_2': 'ERR',
                'rating_1': 'ERR'
            }

        elif len(rating_num) == 0:
            print("No result for " + response.meta['title'])

            yield {
                'movie_id': response.meta['movie_id'],
                'title': response.meta['title'], 
                'url': response.request.url,
                'rating_overall': rating_num.get(),
                'rating_num': 'NA',
                'rating_5': 'NA',
                'rating_4': 'NA',
                'rating_3': 'NA',
                'rating_2': 'NA',
                'rating_1': 'NA'
            }

        else: 
            yield {
                'movie_id': response.meta['movie_id'],
                'title': response.meta['title'], 
                'url': response.request.url,
                'rating_overall': rating_num.get(),
                'rating_num': response.css('a.rating_people span::text').get(),
                'rating_5': response.css('span.rating_per::text')[0].get(),
                'rating_4': response.css('span.rating_per::text')[1].get(),
                'rating_3': response.css('span.rating_per::text')[2].get(),
                'rating_2': response.css('span.rating_per::text')[3].get(),
                'rating_1': response.css('span.rating_per::text')[4].get()
            }
        


        print(str(response.meta['index']) + " / " + str(response.meta['total']))

 