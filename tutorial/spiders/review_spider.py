import os
from time import sleep
from unittest import case
import scrapy
import json
from furl import furl
from datetime import date
import dateparser
from tutorial.items import *
import time


class ReviewSpider(scrapy.Spider):
    name = "review_spider"

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,   
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 4,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1,
        'LOG_LEVEL': 'INFO',
        'COOKIES_ENABLED' : True
    }


    def api_builder(self, project_id, call, page=0):
        #https://movie.douban.com/subject/22265634/comments?start=200&limit=200&status=P&sort=time
        if call == 'top_comments':
            url = 'https://movie.douban.com/subject/' + \
                project_id + '/comments?start=' + str(page * 200) + '&limit=200&status=P'
        elif call == 'comments':
            url = 'https://movie.douban.com/subject/' + \
                project_id + '/comments?start=' + str(page * 200) + '&limit=200&status=P&sort=time'
        else:
            scrapy.exceptions.DropItem("Missing data")
        return url

    def start_requests(self):
        movie_id = self.movie_id
        title = self.title

        url = self.api_builder(movie_id, 'comments', 0)
        yield scrapy.Request(url=url, callback=self.parse, #cookies=cookies,
            meta={'page': 0, 'movie_id': movie_id, 'title': title,
            'playwright': True, "playwright_context": "persistent"})

    def parse(self, response):
        # douban next page exists
        has_next = len(response.css('a.next')) > 0

        page = response.meta['page']
        movid_id = response.meta['movie_id']    
        title = response.meta['title']

        # douban short review
        for review in response.css('div.comment-item'):
            comment_info = review.css('span.comment-info')

            #print(comment_info.css('a'))

            username = comment_info.css('a::text').get()
            user_url = comment_info.css('a::attr(href)').get()
            if user_url is None:
                user_id = ''
                continue
            else:
                user_id = user_url.split('/')[-2]

            rating = review.css('span.rating::attr(title)').get()
            review_text = review.css('span.short::text').get()

            review_dt = review.css('span.comment-time::attr(title)').get()
            review_dt = dateparser.parse(review_dt)
            review_date = review_dt.strftime("%Y-%m-%d")
            review_time = review_dt.strftime("%H:%M:%S")
            
            useful_count = review.css('span.votes::text').get()

            yield {
                'page_index': response.meta['page'],

                'movie_id': movid_id,
                'title': title,
                'username': username,
                'user_id': user_id,
                'rating': rating,
                'date': review_date,
                'time': review_time,
                'comment': review_text,
                'useful_count': useful_count
            }

        if has_next:
            page = page + 1
            next_page = self.api_builder(movid_id, 'comments', page)
            yield scrapy.Request(url=next_page, callback=self.parse, 
                meta={'page': page, 'movie_id': movid_id, 'title': title, 
                'playwright': True, "playwright_context": "persistent"})
        