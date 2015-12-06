from datetime import datetime
import mysql.connector
# from reviews.items import ReviewsItem


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MySQLStorePipeline(object):

    def __init__(self):
        # create an object to check whether the book has been added
        # self.ids_seen = set()
# create a connection object to the database
        self.conn = mysql.connector.connect(user='yourusername', password='yourpassword', database='amazon_crawl')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        now = datetime.now().replace(microsecond=0).isoformat(' ')
        insert_book = ("INSERT INTO reviews "
                       "(review_id, asin, author_id, author_link, author_name,review_link,total_reviews_count,review_date,title,ratings,helpful_votes,total_votes,verified,comments_count,images_count,has_video,text, updated) "
                       "VALUES (%(review_id)s, %(asin)s, %(author_id)s, %(author_link)s, %(author_name)s,%(review_link)s,%(total_reviews_count)s,%(review_date)s,%(title)s,%(ratings)s,%(helpful_votes)s,%(total_votes)s,%(verified)s,%(comments_count)s,%(images_count)s,%(has_video)s,%(text)s, %(updated)s)")
# data object
        data_book = {'review_id': item['review_id'],
                     'asin': item['asin'],
                     'author_id': item['author_id'],
                     'author_link': item['author_link'],
                     'author_name': item['author_name'],
                     'review_link': item['review_link'],
                     'total_reviews_count': item['total_reviews_count'],
                     'review_date': item['review_date'],
                     'title': item['title'],
                     'ratings': item['ratings'],
                     'helpful_votes': item['helpful_votes'],
                     'total_votes': item['total_votes'],
                     'verified': item['verified'],
                     'comments_count': item['comments_count'],
                     'images_count': item['images_count'],
                     'has_video': item['has_video'],
                     'text': item['text'],
                     'updated': now,
                     }
# execute the insert query
        try:
            self.cursor.execute(insert_book, data_book)
            self.conn.commit()
            print bcolors.OKGREEN + "success, inserted into database" + bcolors.ENDC
        except:
            print bcolors.FAIL + "error, not inserted" + bcolors.ENDC
