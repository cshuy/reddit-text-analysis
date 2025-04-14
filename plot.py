#plot
#1.user comment
#2.Cumulative vs Active Comment Authors Over Time
#3.5th Percentile, Median, 95th Percentile
#4.post count bar chart (highly active user to less active) - top 10


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

encodings_to_try = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']

for encoding in encodings_to_try:
    try:
        file_path = 'file path'
        data = pd.read_excel(file_path, encoding=encoding)
        break
    except UnicodeDecodeError:
        continue
    except Exception as e:
        print("Error occurred:", e)
        break

comments_by_author = data['comment_author_username'].value_counts()
percentile_95 = comments_by_author.quantile(0.95)
percentile_99 = comments_by_author.quantile(0.99)

bins = np.linspace(0, comments_by_author.max(), 31)
colors = []
for bin_edge in bins:
    if bin_edge <= percentile_95:
        colors.append('skyblue')
    elif bin_edge <= percentile_99:
        colors.append('orange')
    else:
        colors.append('red')

plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(comments_by_author, bins=bins, edgecolor='black', log=True)
for patch, color in zip(patches, colors[:-1]):
    patch.set_facecolor(color)

plt.title('Frequency Distribution of Number of Comments per Author')
plt.xlabel('Number of Comments')
plt.ylabel('Frequency (Number of Authors)')
plt.show()

print("Number of unique users:", len(comments_by_author))
print("Median number of comments per user:", comments_by_author.median())
print("99th percentile of comments per user:", percentile_99)
print("95th percentile of comments per user:", percentile_95)


file_path = 'file path'
data = pd.read_excel(file_path)
data['comment_created_time'] = pd.to_datetime(data['comment_created_time'])
sorted_data = data.sort_values('comment_created_time')

unique_authors_set = set()
cumulative_counts = []

for index, row in sorted_data.iterrows():
    unique_authors_set.add(row['comment_author_username'])
    cumulative_counts.append(len(unique_authors_set))

sorted_data['Cumulative Unique Authors'] = cumulative_counts

last_comment_date = defaultdict(pd.Timestamp)
for index, row in sorted_data.iterrows():
    last_comment_date[row['comment_author_username']] = row['comment_created_time']

active_counts = []
active_authors = set()
current_date = sorted_data['comment_created_time'].min().date()

for index, row in sorted_data.iterrows():
    if row['comment_created_time'].date() > current_date:
        active_authors = {author for author in active_authors if last_comment_date[author].date() >= current_date}
        current_date = row['comment_created_time'].date()
    
    active_authors.add(row['comment_author_username'])
    active_counts.append(len(active_authors))

sorted_data['Active Authors'] = active_counts

plt.figure(figsize=(12, 6))
plt.plot(sorted_data['comment_created_time'], sorted_data['Cumulative Unique Authors'], color='lightblue', linestyle='-', marker='o', label='Cumulative Unique Authors')
plt.plot(sorted_data['comment_created_time'], sorted_data['Active Authors'], color='darkblue', linestyle='-', marker='x', label='Active Authors')
plt.title('Cumulative vs Active Comment Authors Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Authors')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

post_data = pd.read_excel('file path')
post_data['Created Date'] = pd.to_datetime(post_data['Created Date'])
posts_by_day = post_data['Created Date'].dt.date.value_counts().sort_index()

plt.figure(figsize=(12, 6))
posts_by_day.plot(kind='line', marker='o')
plt.xlabel('Date')
plt.ylabel('Post Count')
plt.title('Temporal Distribution of Posts')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

comment_data = pd.read_excel('file path')
comment_data['comment_created_time'] = pd.to_datetime(comment_data['comment_created_time'])
comments_by_day = comment_data['comment_created_time'].dt.date.value_counts().sort_index()

plt.figure(figsize=(12, 6))
comments_by_day.plot(kind='line', marker='o')
plt.xlabel('Date')
plt.ylabel('Comment Count')
plt.title('Temporal Distribution of Comments')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

file_path = 'file path'
data = pd.read_csv(file_path)
data['Created Date'] = pd.to_datetime(data['Created Date'], format='%Y/%m/%d %H:%M')

post_created_date_comments = data.groupby('Post ID').agg({'Created Date':'min', 'Comment Text':'count'}).rename(columns={'Comment Text': 'Num_Comments'})

percentiles = post_created_date_comments.groupby(post_created_date_comments['Created Date'].dt.date)['Num_Comments'].quantile([0.05, 0.5, 0.95]).unstack()
percentiles = percentiles.reset_index()
percentiles['Created Date'] = pd.to_datetime(percentiles['Created Date'])

plt.figure(figsize=(14, 8))
plt.plot(percentiles['Created Date'], percentiles[0.05], label='5th Percentile', color='lightblue')
plt.plot(percentiles['Created Date'], percentiles[0.5], label='Median (50th Percentile)', color='black')
plt.plot(percentiles['Created Date'], percentiles[0.95], label='95th Percentile', color='lightblue')
plt.title('Daily 5th Percentile, Median, and 95th Percentile of Number of Comments per Post')
plt.xlabel('Date')
plt.ylabel('Number of Comments')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
