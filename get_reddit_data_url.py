#Reddit scraper - Three parts
#1.Save the relevant post URLs using keywords
#2.Download post data using the URLs
#3.Download comment data using the URLs


#Part 1：Save the relevant post URLs using keywords

import praw
import csv
import time
from datetime import datetime

reddit = praw.Reddit(
    client_id='your web app code',
    client_secret='your secret code',
    user_agent='script by /u/name',
)

subreddit_name = "subreddit name"

keyword = "keyword"

subreddit = reddit.subreddit(subreddit_name)

start_date = datetime(2010, 1, 1).timestamp()
end_date = datetime(2024, 2, 29, 23, 59, 59).timestamp()

post_urls = []

search_query = f"title:'{keyword}'"
search_syntax = 'lucene'
search_time_filter = 'all'
search_sort = 'new'
search_limit_per_query = 100

after = None
while True:
    search_results = subreddit.search(query=search_query, syntax=search_syntax, time_filter=search_time_filter, sort=search_sort, limit=search_limit_per_query, params={'after': after})
    for submission in search_results:
        if start_date <= submission.created_utc <= end_date:
            post_urls.append(f"https://www.reddit.com{submission.permalink}")
    after = submission.fullname
    if not after:
        break
    time.sleep(0.5)

csv_file_path = 'file path'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Post URL'])
    for url in post_urls:
        writer.writerow([url])
print("CSV 文件已保存到:", csv_file_path)
