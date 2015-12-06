__author__ = 'Tharun'

from reviews.items import ReviewsItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import csv

with open('amazon_links.csv', 'rU') as file:
    rows = csv.reader(file)
    urls = []
    for row in rows:
        urls.append(row[2])


class ReviewsSpider(CrawlSpider):
    name = "amazon"
    handle_httpstatus_list = [404]
    download_delay = 0.1
    allowed_domains = ["www.amazon.com"]
    #start_urls = (
    #    'http://www.amazon.com/product-reviews/B00M44XD0O',
    #)
    start_urls = list(set(urls))

    rules = (
        # Extract next links and parse them with the spider's method parse_item
        Rule(LinkExtractor(restrict_xpaths=('//li[@class="a-last"]/a',)),
             follow=True, callback='parse_start_url'),
    )

    # def get_largest_sum(self, x):
    #     return [k for k in x.keys() if len(x.get(k)) == max([len(n) for n in x.values()])]

    def parse_start_url(self, response):
        review_count = ''.join(response.xpath('//span[@class="a-size-medium a-text-beside-button totalReviewCount"]/text()').extract()).strip()
        asin = response.url.split("?")[0].split('/')[-1]
        reviews = response.xpath('//div[@id="cm_cr-review_list"]/div[@class="a-section review"]')

        for review in reviews:
            reviewitem = ReviewsItem()
            reviewitem['asin'] = asin
            votes_str = review.xpath('div[@class="a-row helpful-votes-count"]/span/text()').extract()
            if len(votes_str):
                reviewitem['helpful_votes'], reviewitem['total_votes'] = [i.strip().split(" ")[0] for i in votes_str[0].split("of")]
            else:
                reviewitem['helpful_votes'], reviewitem['total_votes'] = 0, 0

            reviewitem['title'] = ''.join(review.xpath('div[@class="a-row"]/a[@class="a-size-base a-link-normal review-title a-color-base a-text-bold"]/text()').extract()).strip()

            review_link = ''.join(review.xpath('div[@class="a-row"]/a[@class="a-size-base a-link-normal review-title '
                                                                   'a-color-base a-text-bold"]/@href').extract()).strip()
            try:
                reviewitem['review_id'] = review_link.split("?")[0].split('/')[-1]
            except:
                reviewitem['review_id'] = ""

            reviewitem['review_link'] = review_link

            reviewitem['author_name'] = ''.join(review.xpath('div[@class="a-row"]/span[@class="a-size-base a-color-secondary review-byline"]/a/text()').extract()).strip()

            author_link = ''.join(review.xpath('div[@class="a-row"]/span[@class="a-size-base a-color-secondary '
                                                                                 'review-byline"]/a/@href').extract()).strip()
            try:
                reviewitem['author_id']=author_link.split("/")[-1]
            except:
                reviewitem['author_id']=""
            reviewitem['author_link'] = author_link
            review_date = review.xpath('div[@class="a-row"]/span[@class="a-size-base a-color-secondary review-date"]/text()').extract()
            if len(review_date):
                reviewitem['review_date'] = review_date[0].split("on")[1].strip()
            else:
                reviewitem['review_date'] = "NULL"

            vp = review.xpath('div[@class="a-row a-spacing-mini review-data"]/span[@class="a-declarative"]/a/span/text()').extract()
            if len(vp):
                reviewitem['verified'] = 1
            else:
                reviewitem['verified'] = 0

            reviewitem['text'] = ''.join(review.xpath('div[@class="a-row review-data"]/span/text()').extract()).strip()

            has_video = review.xpath('div[@class="a-row review-data"]/span/div[@class="a-section a-spacing-small a-spacing-top-mini '
                                     'video-block"]').extract()
            if len(has_video):
                reviewitem['has_video'] = 1
            else:
                reviewitem['has_video'] = 0

            reviewitem['images_count'] = len(review.xpath('div[@class="a-section a-spacing-medium a-spacing-top-medium '
                                              'review-image-container"]/div/img').extract())

            reviewitem['comments_count'] = ''.join(review.xpath('div[@class="a-row a-spacing-top-small review-comments"]/div/a/span/span[\
                    @class="review-comment-total a-hidden"]/text()').extract()).strip()

            reviewitem['total_reviews_count'] = review_count

            ratings = review.xpath('div[@class="a-row"]/a/i/span/text()').extract()

            if len(ratings):
                reviewitem['ratings']=ratings[0].split("out")[0].strip()
            else:
                reviewitem['ratings']=0

            yield reviewitem

        pass

