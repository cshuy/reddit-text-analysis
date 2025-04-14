#sentiment textblob
#1.import packages
#2.preprocessing
#3.sentiment analysis - textblob
#4.plot


import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import nltk
import seaborn as sns
from textblob import TextBlob

nltk.download('stopwords')
nltk.download('wordnet')

data = pd.read_excel("file path")

filtered_data = data[~data['comment_text'].isin(['[deleted]', '[removed]'])]

def nacs_lemmatize(word):
    exclude_terms = {'ccs'}
    if word.lower() in exclude_terms:
        return word
    elif word.lower() == 'nacs':
        return 'nacs'
    else:
        lemmatizer = WordNetLemmatizer()
        return lemmatizer.lemmatize(word)

def clean_text(text):
    if pd.isnull(text):
        return ''
    text = re.sub(r'^>.*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'http\S+|www\S+|https?://\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'giphy\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    emoji_pattern = re.compile("[" 
                       u"\U0001F600-\U0001F64F"  
                       u"\U0001F300-\U0001F5FF"  
                       u"\U0001F680-\U0001F6FF"  
                       u"\U0001F1E0-\U0001F1FF"  
                       u"\U00002702-\U000027B0"
                       u"\U000024C2-\U0001F251"
                       "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    text = ' '.join([nacs_lemmatize(word) for word in text.split()])
    return text.strip()

filtered_data['cleaned_comments'] = filtered_data['comment_text'].apply(clean_text)
filtered_data = filtered_data[filtered_data['cleaned_comments'] != '']

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

filtered_data['textblob_score'] = filtered_data['cleaned_comments'].apply(analyze_sentiment)

plt.hist(filtered_data['textblob_score'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.title('Distribution of Sentiment Polarity')
plt.grid(True)
plt.show()

filtered_data['comment_created_time'] = pd.to_datetime(filtered_data['comment_created_time'])

grouped_data = filtered_data.groupby(['Post ID', 'comment_created_time'])['textblob_score'].mean().reset_index()

specific_post_ids = ['13ruz59']
grouped_data = grouped_data[grouped_data['Post ID'].isin(specific_post_ids)]

plt.figure(figsize=(12, 8))

for post_id, group in grouped_data.groupby('Post ID'):
    plt.plot(group['comment_created_time'], group['textblob_score'], label=post_id, marker='o', linestyle='-', markersize=5)

plt.xlabel('comment_created_time')
plt.ylabel('Average Sentiment Score')
plt.title('Trend of Sentiment Score by Post ID over Time')
plt.legend(title='Post ID', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

filtered_data['comment_created_time'] = pd.to_datetime(filtered_data['comment_created_time'])

filtered_data['date'] = filtered_data['comment_created_time'].dt.date

daily_sentiment = filtered_data.groupby('date')['textblob_score'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(daily_sentiment['date'], daily_sentiment['textblob_score'], marker='o', linestyle='-')
plt.xlabel('Date')
plt.ylabel('Average Sentiment Score')
plt.title('Daily Average Sentiment Score Over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

filtered_data['comment_created_time'] = pd.to_datetime(filtered_data['comment_created_time'])

filtered_data['date'] = filtered_data['comment_created_time'].dt.date

cutoff1 = pd.to_datetime('2022-11-11').date()
cutoff2 = pd.to_datetime('2023-05-25').date()

data_before_cutoff1 = filtered_data[filtered_data['date'] < cutoff1]
data_between_cutoffs = filtered_data[(filtered_data['date'] >= cutoff1) & (filtered_data['date'] <= cutoff2)]
data_after_cutoff2 = filtered_data[filtered_data['date'] > cutoff2]

def compute_daily_sentiment(data):
    return data.groupby('date')['textblob_score'].mean().reset_index()

daily_sentiment_before_cutoff1 = compute_daily_sentiment(data_before_cutoff1)
daily_sentiment_between_cutoffs = compute_daily_sentiment(data_between_cutoffs)
daily_sentiment_after_cutoff2 = compute_daily_sentiment(data_after_cutoff2)

def plot_sentiment(daily_sentiment, title, filename):
    plt.figure(figsize=(12, 6))
    plt.plot(daily_sentiment['date'], daily_sentiment['textblob_score'], marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Average Sentiment Score')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

plot_sentiment(daily_sentiment_before_cutoff1, 'Sentiment Score Before 2022-11-11', 'sentiment_before_cutoff1.png')
plot_sentiment(daily_sentiment_between_cutoffs, 'Sentiment Score Between 2022-11-11 and 2023-05-25', 'sentiment_between_cutoffs.png')
plot_sentiment(daily_sentiment_after_cutoff2, 'Sentiment Score After 2023-05-25', 'sentiment_after_cutoff2.png')
