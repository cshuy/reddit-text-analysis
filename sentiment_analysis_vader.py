#sentiment vader
#1.import packages
#2.preprocessing
#3.sentiment analysis - vader


import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import nltk
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

data = pd.read_excel("file path")

filtered_data = data[~data['comment_text'].isin(['[deleted]', '[removed]'])]

def clean_text(text):
    if pd.isnull(text):
        return ''
    text = re.sub(r'^(?:>.*(?:\n|$))+', '', text, flags=re.MULTILINE)
    text = re.sub(r'(https?://\S+|www\.\S+|\[.*?\]\(.*?\))', '', text)
    text = re.sub(r'giphy\S+', '', text)
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

filtered_data['cleaned_comments'] = filtered_data['comment_text'].apply(clean_text)
filtered_data = filtered_data[filtered_data['cleaned_comments'] != '']

sid = SentimentIntensityAnalyzer()

def get_sentiment_scores(text):
    return sid.polarity_scores(text)

filtered_data['vader_scores'] = filtered_data['cleaned_comments'].apply(get_sentiment_scores)

filtered_data['compound_score'] = filtered_data['vader_scores'].apply(lambda x: x['compound'])

def categorize_sentiment(score):
    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    else:
        return 'neutral'

filtered_data['sentiment'] = filtered_data['compound_score'].apply(categorize_sentiment)
