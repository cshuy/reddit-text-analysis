#Reddit scraper - Three Parts
#1.Save the relevant post URLs using keywords
#2.Download post data using the URLs
#3.Download comment data using the URLs


#Part 3：Download comment data using the URLs

import praw
import pandas as pd
import openpyxl
from datetime import datetime
import time

excel_file = "file path"
df = pd.read_excel(excel_file)

reddit = praw.Reddit(
    client_id='your web app code',
    client_secret='your secret code',
    user_agent='script by /u/name',
)

comments_data = []

for index, row in df.iterrows():
    url = row['Post URL']
    submission_id = url.split('/')[-3]
    try:
        submission = reddit.submission(id=submission_id)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            comment_text = comment.body if comment.body else "Deleted or Removed"
            author_username = comment.author.name if comment.author else "N/A"
            comment_created_time = datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            try:
                author_cake_day = datetime.utcfromtimestamp(comment.author.created_utc).strftime('%Y-%m-%d %H:%M:%S') if comment.author else "N/A"
            except AttributeError:
                author_cake_day = "N/A"            
            comments_data.append({'URL': url,
                                  'comment_text': comment_text,
                                  'comment_created_time': comment_created_time,
                                  'comment_score': comment.score,
                                  'comment_author_username': author_username,
                                  'comment_author_cake_day': author_cake_day})
            time.sleep(3)
    except Exception as e:
        print(f"Error processing {url}: {e}")
        
comments_df = pd.DataFrame(comments_data)
output_excel_file = "file path"
comments_df.to_excel(output_excel_file, index=False)
print("CSV 文件已保存到:", csv_file_path)