#Reddit scraper - Three parts
#1.Save the relevant post URLs using keywords
#2.Download post data using the URLs
#3.Download comment data using the URLs


#Part 2：Download post data using the URLs

import praw
import pandas as pd
from datetime import datetime

reddit = praw.Reddit(
    client_id='your web app code',
    client_secret='your secret code',
    user_agent='script by /u/name',
)

excel_file_path = 'file path'
df = pd.read_excel(excel_file_path)

posts_info = []
for url in df['Post URL']:
    submission = reddit.submission(url=url)
    try:
        post_author_cake_day = datetime.utcfromtimestamp(reddit.redditor(submission.author.name).created_utc).strftime('%Y-%m-%d')
    except AttributeError:
        post_author_cake_day = 'N/A'
    
    post_info = {
        'Subreddit': submission.subreddit.display_name,
        'Post Flair': submission.link_flair_text if submission.link_flair_text else 'N/A',
        'Post ID': submission.id,
        'Post Title': submission.title,
        'Post Text': submission.selftext,
        'URL in post': submission.url,
        'Created Date': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        'Created Year': datetime.utcfromtimestamp(submission.created_utc).strftime('%Y'),
        'Score': submission.score,
        'Number of Comments': submission.num_comments,
        'Post Author Username': submission.author.name if submission.author else 'N/A',
        'URL': f"https://www.reddit.com{submission.permalink}",
    }
    posts_info.append(post_info)


df_result = pd.DataFrame(posts_info)
output_excel_file_path = 'file path'
df_result.to_excel(output_excel_file_path, index=False)
print("Excel 文件已保存到:", output_excel_file_path)