#similarity
#1.import packages
#2.preprocessing
#3.Categorize data: formal-leader / informal-leader / non-leader
#4.Extract segment data based on time and subreddit into new lists
#5.Convert text to string
#6.Cosine Similarity、Jaccard Similarity、Delta Method


import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import nltk
import spacy

filtered_data = pd.read_excel("file path")

def clean_text(text):
    if pd.isnull(text):
        return ''
    text = re.sub(r'\!\[img\]\(.*?\)', '', text)
    text = re.sub(r'http\S+|www\S+|https?://\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'giphy\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^A-Za-z\s.,!?]', '', text)
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
    return text.strip()

filtered_data['cleaned_comments'] = filtered_data['comment_text'].apply(clean_text)
filtered_data = filtered_data[filtered_data['cleaned_comments'] != '']

formal_leader_list = pd.read_excel("file path")

formal_leader_data = []
for index, row in formal_leader_list.iterrows():
    subreddit = row['Subreddit']
    username = row['username']
    matched_data = filtered_data[(filtered_data['Subreddit'] == subreddit) & 
                                 (filtered_data['comment_author_username'] == username)]
    if not matched_data.empty:
        formal_leader_data.append(matched_data)

formal_leader_data = pd.concat(formal_leader_data, ignore_index=True)

informal_leader_list = pd.read_excel("file path")

informal_leader_data = []
for index, row in informal_leader_list.iterrows():
    subreddit = row['subreddit']
    period = row['period']
    username = row['username']
    matched_data = filtered_data[(filtered_data['Subreddit'] == subreddit) & 
                                 (filtered_data['period'] == period) & 
                                 (filtered_data['comment_author_username'] == username)]
    if not matched_data.empty:
        informal_leader_data.append(matched_data)

informal_leader_data = pd.concat(informal_leader_data, ignore_index=True)

non_leader_data = filtered_data[~filtered_data['comment_author_username'].isin(formal_leader_list['username'])]
non_leader_data = non_leader_data[~non_leader_data['comment_author_username'].isin(informal_leader_list['username'])]

def extract_data_by_subreddit_and_period(df, subreddit, period):
    return df[(df['Subreddit'] == subreddit) & (df['period'] == period)]

cars01_formal_leader_data = extract_data_by_subreddit_and_period(formal_leader_data, 'teslamotors', 3)
cars01_informal_leader_data = extract_data_by_subreddit_and_period(informal_leader_data, 'teslamotors', 3)
cars01_non_leader_data = extract_data_by_subreddit_and_period(non_leader_data, 'teslamotors', 3)

cars01_formal_leader_comments = ' '.join(cars01_formal_leader_data['cleaned_comments'])
cars01_informal_leader_comments = ' '.join(cars01_informal_leader_data['cleaned_comments'])
cars01_non_leader_comments = ' '.join(cars01_non_leader_data['cleaned_comments'])

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

tfidf_vectorizer = TfidfVectorizer()

texts = [cars01_formal_leader_comments, cars01_informal_leader_comments, cars01_non_leader_comments]

tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

formal_vs_non_leader_sim = cosine_similarities[0, 2]
formal_vs_informal_sim = cosine_similarities[0, 1]
informal_vs_non_leader_sim = cosine_similarities[1, 2]

print(f"Cosine Similarity Formal Leader vs Non-Leader: {formal_vs_non_leader_sim:.4f}")
print(f"Cosine Similarity Formal Leader vs Informal Leader: {formal_vs_informal_sim:.4f}")
print(f"Cosine Similarity Informal Leader vs Non-Leader: {informal_vs_non_leader_sim:.4f}")

def jaccard_similarity(doc1, doc2):
    words_doc1 = set(doc1.split())
    words_doc2 = set(doc2.split())
    intersection = words_doc1.intersection(words_doc2)
    union = words_doc1.union(words_doc2)
    jaccard_index = float(len(intersection)) / len(union)
    return jaccard_index

jaccard_sim_formal_non_leader = jaccard_similarity(cars01_formal_leader_comments, cars01_non_leader_comments)
jaccard_sim_formal_informal = jaccard_similarity(cars01_formal_leader_comments, cars01_informal_leader_comments)
jaccard_sim_informal_non_leader = jaccard_similarity(cars01_informal_leader_comments, cars01_non_leader_comments)

print(f"Jaccard Similarity Formal Leader vs Non-Leader: {jaccard_sim_formal_non_leader:.4f}")
print(f"Jaccard Similarity Formal Leader vs Informal Leader: {jaccard_sim_formal_informal:.4f}")
print(f"Jaccard Similarity Informal Leader vs Non-Leader: {jaccard_sim_informal_non_leader:.4f}")

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from scipy.stats import zscore

def calculate_delta(text1, text2, top_n=100):
    vectorizer = CountVectorizer(stop_words='english')
    frequencies = vectorizer.fit_transform([text1, text2]).toarray()
    total_counts = np.sum(frequencies, axis=0)
    top_indices = np.argsort(total_counts)[::-1][:top_n]
    top_frequencies = frequencies[:, top_indices]
    z_scores = zscore(top_frequencies, axis=1)
    delta = np.mean(np.abs(z_scores[0] - z_scores[1]))
    return delta

delta_formal_non_leader = calculate_delta(cars01_formal_leader_comments, cars01_non_leader_comments)
delta_formal_informal = calculate_delta(cars01_formal_leader_comments, cars01_informal_leader_comments)
delta_informal_non_leader = calculate_delta(cars01_informal_leader_comments, cars01_non_leader_comments)

print(f"Delta Formal Leader vs Non-Leader: {delta_formal_non_leader:.4f}")
print(f"Delta Formal Leader vs Informal Leader: {delta_formal_informal:.4f}")
print(f"Delta Informal Leader vs Non-Leader: {delta_informal_non_leader:.4f}")
