# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewsItem(scrapy.Item):
    # define the fields for your item here like:
    review_id = scrapy.Field()
    asin = scrapy.Field()
    author_id = scrapy.Field()
    author_link = scrapy.Field()
    author_name = scrapy.Field()
    review_link = scrapy.Field()
    total_reviews_count = scrapy.Field()
    review_date = scrapy.Field()
    title = scrapy.Field()
    ratings = scrapy.Field()
    helpful_votes = scrapy.Field()
    total_votes = scrapy.Field()
    verified = scrapy.Field()
    comments_count = scrapy.Field()
    images_count = scrapy.Field()
    has_video = scrapy.Field()
    text = scrapy.Field()
    pass
