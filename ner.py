#NER
#1.import packages
#2.preprocessing
#3.NER
#4.plot


import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import nltk
import spacy

nlp = spacy.load("en_core_web_lg")
nltk.download('stopwords')
nltk.download('wordnet')

data = pd.read_excel("fiel path")
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


def recognize_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ not in {'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'}:
            entities.append((ent.text, ent.label_))
    return len(entities)

def prepare_and_plot(data):
    data['comment_created_time'] = pd.to_datetime(data['comment_created_time'])
    data['entity_count'] = data['cleaned_comments'].apply(recognize_entities)
    data['date'] = data['comment_created_time'].dt.date
    daily_entity_counts = data.groupby('date')['entity_count'].sum()
    plt.figure(figsize=(12, 6))
    daily_entity_counts.plot(kind='line')
    plt.title('Number of Recognized Entities Over Time')
    plt.xlabel('Time')
    plt.ylabel('Count of Recognized Entities')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
prepare_and_plot(filtered_data)



def recognize_entities(text, timestamp, exclude_labels=None):
    if exclude_labels is None:
        exclude_labels = {'DATE', 'TIME', 'PERCENT', 'MONEY', 'QUANTITY', 'ORDINAL', 'CARDINAL'}
    
    doc = nlp(text)
    entities_with_time = []
    for ent in doc.ents:
        if ent.label_ not in exclude_labels:
            entities_with_time.append({
                'entity': ent.text,
                'label': ent.label_,
                'comment_created_time': timestamp
            })
    return entities_with_time

all_entities = []

for index, row in filtered_data.iterrows():
    entities = recognize_entities(row['comment_text'], row['comment_created_time'])
    all_entities.extend(entities)

entities_df = pd.DataFrame(all_entities)
entities_df.to_excel("file path", index=False)
print(entities_df.head())



from collections import defaultdict

entities_df = pd.read_excel("file path")
entities_df['comment_created_time'] = pd.to_datetime(entities_df['comment_created_time'])
sorted_entities = entities_df.sort_values('comment_created_time')
unique_entities_set = set()
cumulative_counts = []

for index, row in sorted_entities.iterrows():
    unique_entities_set.add(row['entity'])
    cumulative_counts.append(len(unique_entities_set))

sorted_entities['Cumulative Unique Entities'] = cumulative_counts
last_entity_date = defaultdict(pd.Timestamp)

for index, row in sorted_entities.iterrows():
    last_entity_date[row['entity']] = row['comment_created_time']

active_counts = []
active_entities = set()

current_date = sorted_entities['comment_created_time'].min().date()

for index, row in sorted_entities.iterrows():
    if row['comment_created_time'].date() > current_date:
        active_entities = {entity for entity in active_entities if last_entity_date[entity].date() >= current_date}
        current_date = row['comment_created_time'].date()
    
    active_entities.add(row['entity'])
    active_counts.append(len(active_entities))

sorted_entities['Active Entities'] = active_counts

plt.figure(figsize=(12, 6))
plt.plot(sorted_entities['comment_created_time'], sorted_entities['Cumulative Unique Entities'], color='lightblue', linestyle='-', marker='o', label='Cumulative Unique Entities')
plt.plot(sorted_entities['comment_created_time'], sorted_entities['Active Entities'], color='darkblue', linestyle='-', marker='x', label='Active Entities')
plt.title('Cumulative vs Active Entities Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Entities')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
