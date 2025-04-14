#readability
#1.import packages
#2.preprocessing
#3.Categorize data: formal-leader / informal-leader / non-leader
#4.Extract segment data based on time and subreddit into new lists
#5.Readability (Flesch-Kincaid Grade Level) / plot
#6.Readability (Automated Readability Index - ARI) / plot


import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import nltk
import spacy
import textstat
import numpy as np

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

def calculate_flesch_kincaid(df):
    df['flesch_kincaid_grade'] = df['cleaned_comments'].apply(textstat.flesch_kincaid_grade)
    return df.groupby('comment_author_username')['flesch_kincaid_grade'].mean().reset_index()

cars01_formal_leader_fk = calculate_flesch_kincaid(cars01_formal_leader_data)
cars01_informal_leader_fk = calculate_flesch_kincaid(cars01_informal_leader_data)
cars01_non_leader_fk = calculate_flesch_kincaid(cars01_non_leader_data)

def plot_flesch_kincaid_histograms(df1, df2, df3):
    plt.figure(figsize=(10, 6))
    all_scores = pd.concat([df1['flesch_kincaid_grade'], df2['flesch_kincaid_grade'], df3['flesch_kincaid_grade']])
    labels = ['Formal-Leader'] * len(df1) + ['Informal-Leader'] * len(df2) + ['Non-Leader'] * len(df3)
    plot_data = pd.DataFrame({
        'Flesch-Kincaid Grade Level': all_scores,
        'Group': labels
    })
    for label, group in plot_data.groupby('Group'):
        plt.hist(group['Flesch-Kincaid Grade Level'], bins=np.linspace(-0, 175, 40), alpha=0.5, label=label)

    median_formal = df1['flesch_kincaid_grade'].median()
    median_informal = df2['flesch_kincaid_grade'].median()
    median_non_leader = df3['flesch_kincaid_grade'].median()

    plt.axvline(median_formal, color='blue', linestyle='dashed', linewidth=1, label=f'Median (Formal-Leader): {median_formal:.2f}')
    plt.axvline(median_informal, color='purple', linestyle='dashed', linewidth=1, label=f'Median (Informal-Leader): {median_informal:.2f}')
    plt.axvline(median_non_leader, color='red', linestyle='dashed', linewidth=1, label=f'Median (Non-Leader): {median_non_leader:.2f}')

    plt.yscale('log')
    plt.xlabel('Flesch-Kincaid Grade Level')
    plt.ylabel('Frequency (log scale)')
    plt.title('Distribution of Flesch-Kincaid Grade Level Scores')
    plt.legend()
    plt.grid(True)
    plt.show()

plot_flesch_kincaid_histograms(cars01_formal_leader_fk, cars01_informal_leader_fk, cars01_non_leader_fk)

def calculate_ari(df):
    df['ari'] = df['cleaned_comments'].apply(textstat.automated_readability_index)
    return df.groupby('comment_author_username')['ari'].mean().reset_index()

cars01_formal_leader_ari = calculate_ari(cars01_formal_leader_data)
cars01_informal_leader_ari = calculate_ari(cars01_informal_leader_data)
cars01_non_leader_ari = calculate_ari(cars01_non_leader_data)

def plot_ari_histograms(df1, df2, df3):
    plt.figure(figsize=(10, 6))
    all_scores = pd.concat([df1['ari'], df2['ari'], df3['ari']])
    labels = ['Formal-Leader'] * len(df1) + ['Informal-Leader'] * len(df2) + ['Non-Leader'] * len(df3)
    plot_data = pd.DataFrame({
        'ARI': all_scores,
        'Group': labels
    })
    for label, group in plot_data.groupby('Group'):
        plt.hist(group['ARI'], bins=np.linspace(-0, 50, 40), alpha=0.5, label=label)

    median_formal = df1['ari'].median()
    median_informal = df2['ari'].median()
    median_non_leader = df3['ari'].median()

    plt.axvline(median_formal, color='blue', linestyle='dashed', linewidth=1, label=f'Median (Formal-Leader): {median_formal:.2f}')
    plt.axvline(median_informal, color='purple', linestyle='dashed', linewidth=1, label=f'Median (Informal-Leader): {median_informal:.2f}')
    plt.axvline(median_non_leader, color='red', linestyle='dashed', linewidth=1, label=f'Median (Non-Leader): {median_non_leader:.2f}')

    plt.yscale('log')
    plt.xlabel('Automated Readability Index (ARI)')
    plt.ylabel('Frequency (log scale)')
    plt.title('Distribution of Automated Readability Index Scores')
    plt.legend()
    plt.grid(True)
    plt.show()

plot_ari_histograms(cars01_formal_leader_ari, cars01_informal_leader_ari, cars01_non_leader_ari)
