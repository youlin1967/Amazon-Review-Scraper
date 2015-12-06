# -*- coding: utf-8 -*-

BOT_NAME = 'reviews'

SPIDER_MODULES = ['reviews.spiders']
NEWSPIDER_MODULE = 'reviews.spiders'
DEFAULT_ITEM_CLASS = 'reviews.items.ReviewsItem'

ITEM_PIPELINES = [
     'reviews.pipelines.MySQLStorePipeline',
]

DOWNLOAD_HANDLERS = {
  's3': None,
}
