DROP TABLE IF EXISTS reviews;
CREATE TABLE amazon_crawl.reviews (
review_id varchar(255) PRIMARY KEY,
asin varchar(255),
author_id varchar(255),
author_link varchar(255),
author_name varchar(255),
review_link varchar(255),
total_reviews_count int,
review_date varchar(255),
title text,
ratings double,
helpful_votes int,
total_votes int,
verified int,
comments_count int,
images_count int,
has_video int,
text text,
updated datetime
) DEFAULT CHARSET=utf8;
