#Wordcloud
#1.import packages
#2.preprocessing
#3.tf-idf & n-gram & wordcloud


import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud

nltk.download('stopwords')
nltk.download('wordnet')

data = pd.read_excel("file path")

filtered_data = data[~data['comment_text'].isin(['[deleted]', '[removed]'])]

alias_dict = {
    'super charger': 'supercharger',
    'sc': 'supercharger',
    'combine charging system': 'CCS',
    'North American Charging Standard': 'NACS',
    'Tesla charging standard': 'TCS',
    'CHArge de MOve': 'CHAdeMO'
}

def nacs_lemmatize(word):
    exclude_terms = {'ccs'}
    if word.lower() in exclude_terms:
        return word
    elif word.lower() == 'nacs':
        return 'nacs'
    else:
        lemmatizer = WordNetLemmatizer()
        return lemmatizer.lemmatize(word)

def harmonize_aliases(text):
    for key, value in alias_dict.items():
        text = re.sub(r'\b' + re.escape(key) + r'\b', value, text, flags=re.IGNORECASE)
    return text

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

for comment in filtered_data['cleaned_comments'].head(10):
    print(comment)

def generate_tfidf_word_clouds(filtered_data):
    filtered_data['comment_created_time'] = pd.to_datetime(filtered_data['comment_created_time'])
    tfidf_vectorizer = TfidfVectorizer(max_features=1000000, ngram_range=(1, 3))
    tfidf_features = tfidf_vectorizer.fit_transform(filtered_data['cleaned_comments'])
    dates = filtered_data['comment_created_time']
    nov_2022_cutoff = pd.Timestamp('2022-11-11')
    may_2023_cutoff = pd.Timestamp('2023-05-25')
    before_indices = dates < nov_2022_cutoff
    between_indices = (dates >= nov_2022_cutoff) & (dates < may_2023_cutoff)
    after_indices = dates >= may_2023_cutoff
    tfidf_before = tfidf_features[before_indices]
    tfidf_between = tfidf_features[between_indices]
    tfidf_after = tfidf_features[after_indices]
    tfidf_before_means = tfidf_before.mean(axis=0)
    tfidf_between_means = tfidf_between.mean(axis=0)
    tfidf_after_means = tfidf_after.mean(axis=0)
    words = tfidf_vectorizer.get_feature_names_out()
    tfidf_before_dict = {words[i]: tfidf_before_means[0, i] for i in range(len(words))}
    tfidf_between_dict = {words[i]: tfidf_between_means[0, i] for i in range(len(words))}
    tfidf_after_dict = {words[i]: tfidf_after_means[0, i] for i in range(len(words))}
    wordcloud_before = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(tfidf_before_dict)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_before, interpolation='bilinear')
    plt.title('TF-IDF Word Cloud for Comments Before Nov 2022')
    plt.axis('off')
    plt.show()

    wordcloud_between = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(tfidf_between_dict)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_between, interpolation='bilinear')
    plt.title('TF-IDF Word Cloud for Comments Between Nov 2022 and May 2023')
    plt.axis('off')
    plt.show()

    wordcloud_after = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(tfidf_after_dict)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud_after, interpolation='bilinear')
    plt.title('TF-IDF Word Cloud for Comments After May 2023')
    plt.axis('off')
    plt.show()

generate_tfidf_word_clouds(filtered_data)

filtered_data['comment_created_time'] = pd.to_datetime(filtered_data['comment_created_time'])

filtered_data['ccs_count'] = filtered_data['cleaned_comments'].str.contains('ccs').astype(int)
filtered_data['nacs_count'] = filtered_data['cleaned_comments'].str.contains('nacs').astype(int)

time_grouped = filtered_data.resample('M', on='comment_created_time').agg({'ccs_count': 'sum', 'nacs_count': 'sum'})

plt.figure(figsize=(14, 7))
plt.plot(time_grouped.index, time_grouped['ccs_count'], label='CCS', marker='o')
plt.plot(time_grouped.index, time_grouped['nacs_count'], label='NACS', marker='o')

plt.title('Frequency of CCS and NACS Over Time')
plt.xlabel('Date')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()
