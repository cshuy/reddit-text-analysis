This portfolio showcases various text analysis techniques implemented in Python, including:

- **Web Scraping (Reddit API)**: Extraction of text data from Reddit posts and comments using the official Reddit API.
- **Preprocessing**: Cleaning and preparing text data for analysis.
- **Text Analysis**:
	- **Word Cloud:** Visual representation of the most frequent words.
	- **Sentiment Analysis**: Classifying the sentiment of text (positive, negative, neutral).
	- **Named Entity Recognition (NER)**: Identifying key entities such as names, locations, and dates in text.
	- **Text Similarity**: Measuring the semantic similarity between different pieces of text.
	- **Readability Analysis**: Assessing the ease with which the text can be read and understood.

This project is aimed at demonstrating practical applications of Natural Language Processing (NLP) and Data Analysis techniques.

# Project Background
The characteristics of online communities attract numerous participants. However, the interactions among these participants can lead to tensions and conflicts. Therefore, leaders take specific roles in alleviating the community atmosphere. This study uses text analysis to explore how leaders in online communities take these roles and what language styles they use to influence the community.

On November 11th, 2022, Tesla announced that it would open up the North American Charging Standard (NACS) to other manufacturers. Prior to this, various connectors, such as CCS and CHAdeMO, co-existed in the North American electric vehicle charging ecosystem. Despite Tesla’s streamlined charging technology, adopting a single standard raised various concerns. By May 25th, 2023, Ford Motor Company announced its intention to adopt the NACS standard, followed by other automakers expressing similar plans, further fueling online discussions and debates.

Insights and recommendations are provided on the following key areas:

- **Category 1:** Community discussion trends
- **Category 1:** How leaders in online communities assume their roles
- **Category 2:** The language styles they use to influence the community

Here is the analysis workflow for my project:
![workflow](https://github.com/cshuy/reddit-text-analysis/blob/fac2e2727e4bb8af7b58a59e2b19c35915e9bc51/method.png)

# Data Structure & Initial Checks
We collected data using the official Reddit API, specifically the Python Reddit API Wrapper. We selected three public subreddits: "r/electricvehicles," "r/teslamotors," and "r/cars."A description of each table is as follows:

| Subreddit        | From       | Until      | Comment count |
| ---------------- | ---------- | ---------- | ------------- |
| cars             | 2012-02-09 | 2024-02-12 | 6,771         |
| electricvehicles | 2013-07-11 | 2024-02-29 | 39,484        |
| teslamotors      | 2014-04-09 | 2024-02-29 | 35,495        |
| **Total**        | 2012-02-09 | 2024-02-29 | **81,750**    |

Note: The time distribution of the data we collected from these subreddits.

Here is the ERD (Entity Relationship Diagram) of my tables:
![ERD](https://github.com/cshuy/reddit-text-analysis/blob/5263cda47011909cc69e8ecffce9bcbb53235ca4/erd_reddit.jpg)

We applied different preprocessing steps based on various analysis methods, as shown in the table below:

| Analysis                         | Pre-processing steps                                                                                                                                                                                                                                                                            |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Word cloud                       | Step 1: Alias harmonization dictionary<br>Step 2: Removed quotes, links, images, gifs, special symbols and emoji<br>Step 3: Lowercase<br>Step 4: Tokenization<br>Step 5: Lemmatize<br>Step 6: Remove stop words<br>Step 7: Term Frequency-Inverse Document Frequency (Tf-idf)<br>Step 8: N-gram |
| NER                              | Step 1: Define custom lemmatization function (e.g., NACS, CCS)<br>Step 2: Remove quotes, links, images, gifs, special symbols and emoji<br>Step 3: Lowercase<br>Step 4: Tokenization<br>Step 5: Lemmatize<br>Step 6: Remove stop words                                                          |
| Sentiment analysis<br>(Textblob) | Step 1: Define custom lemmatization function (e.g., NACS, CCS)<br>Step 2: Remove quotes, links, images, gifs, special symbols and emoji<br>Step 3: Lowercase<br>Step 4: Tokenization<br>Step 5: Lemmatize<br>Step 6: Remove stop words                                                          |
| Sentiment analysis<br>(VADER)    | Step 1: Remove quotes, links, images, gifs, special symbols<br>Step 2: Tokenization<br>Step 3: Remove stop words                                                                                                                                                                                |
| Text readability                 | Step 1: Remove quotes, links, images, gifs, special symbols, emojis<br>Step 2: Lowercase                                                                                                                                                                                                        |
| Text similarity                  | Step 1: Remove quotes, links, images, gifs, special symbols, emojis<br>Step 2: Lowercase                                                                                                                                                                                                        |
# Executive Summary

### Overview of Findings

This study highlights the significant influence of online community leaders in shaping discussions about the North American Charging Standard (NACS). Key findings show that formal and informal leaders play crucial roles in organizing, mediating, and guiding the community's views on charging standards. Additionally, consumer sentiment surrounding NACS evolved over time, with initial skepticism transforming into growing support as more automotive brands, like Ford, announced their adoption of the standard. For automotive brands, it is evident that actively engaging with and understanding these online discussions is vital for aligning strategies with consumer preferences and industry trends.

# Insights Deep Dive
### Category 1: Community discussion trends

* **Main insight 1.** While other charging standards gradually diminish or disappear, discussions increasingly focus on NACS.
![Word cloud](https://github.com/cshuy/reddit-text-analysis/blob/d92e2996aded19033de4927fc2b3141c601b7278/word%20cloud.png)

* **Main insight 2.** There is a notable increase in the number of posts and comments about NACS from June 2023 to September 2023. During this period, several automotive manufacturers announced their adoption of NACS, sparking interest and discussion within the Reddit community.
![Temporal disribution of posts](https://github.com/cshuy/reddit-text-analysis/blob/5263cda47011909cc69e8ecffce9bcbb53235ca4/temporal%20disribution%20of%20posts.png)

### Category 2: How leaders in online communities assume their roles

* **Main insight 1.** There is no obvious difference in sentiment score, and most of them are concentrated in neutral.
  
* **Main insight 2.** Formal leaders and informal leaders use entities more often than non-leaders.


### Category 3: The language styles they use to influence the community

* **Main insight 1.** Leaders user more sophisticated language
  
* **Main insight 2.** Informal leaders use  similar languages with non-leaders

### Summary of finding

This study’s summary of findings is outlined in the table below:

| **Roles**           | **Mediator**                                                                                                                      | **Organizer**                                                                                                                                                                     | **Language style**                                                                                                                                                          |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Formal Leader**   | 1.More positive sentiment score<br><br>(Observed official roles)<br><br>1.Make subreddit's rules<br>2.Remove comments and members | 1.Entities are used more frequently<br><br>(Observed official roles)  <br><br>1.Post weekly information<br>2.Maintain community database<br>3.Write FAQs<br>4.Pin important posts | 1.Longer average sentence length<br><br>2.Higher average word complexity<br><br>3.Higher readability scores (difficult)<br><br>4.Language style less similar to non-leaders |
| **Informal Leader** | 1.More positive sentiment score<br><br>(Observed official roles)  <br>  <br>1.Posting important information                       | 1.Entities are used more frequently                                                                                                                                               | 1. Language style similar to non-leader.<br><br>2.Higher average word complexity<br><br>3.Higher readability scores (difficult)                                             |
| Non-Leader          | 1.More natural sentiment scores                                                                                                   | 1.Entities are used less frequently                                                                                                                                               | 1.Lower readability scores(simpler)<br><br>2.Shorter average sentence                                                                                                       |


# Recommendations:

Based on the analysis, the following strategic considerations could be relevant for **industry stakeholders** and **regulatory bodies**:

- **Multiple EV charging standards hinder adoption**  
    → Prioritize the development of a unified charging standard to simplify the user experience and accelerate EV growth.
    
- **Lack of consumer involvement in standardization may cause dissatisfaction**  
    → Ensure transparency by providing open forums or surveys for public input during the standardization process.
    
- **Fragmented infrastructure investments waste resources**  
    → Encourage collaboration between public and private sectors to streamline charging station planning and resource allocation.
    
- **Tesla’s NACS adoption signals market shift**  
    → Monitor industry trends and assess the potential adoption of NACS as a primary standard, ensuring a smooth transition for CCS users.
    
- **Online communities influence public perception**  
    → Engage with online communities to address misinformation, collect feedback, and shape communication strategies.
  
# Assumptions and Caveats:

Throughout the analysis, multiple assumptions were made to manage challenges with the data. These assumptions and caveats are noted below:

- **Moderator data limitation**: Reddit only provides the current list of moderators. We assumed that current moderators are indicative of long-term community leadership.
    
- **Bot filtering**: Only known bot accounts were removed using existing labeled data. Undetected bots or coordinated actors may still influence community sentiment and discussion trends.
    
- **Data coverage**: Analysis was limited to selected keywords and subreddits. Relevant discussions outside the scope may have been missed, potentially affecting the completeness of insights.
    
- **Leader definition**: Informal leaders were identified using influence-based metrics (top 1%). Some influential users may have been overlooked due to thresholding.
    
- **Model limitations**: Pre-trained NLP models were used for sentiment and entity analysis. These may misinterpret domain-specific language, sarcasm, or emerging internet slang.
    
- **Event-specific focus**: The analysis centers around a specific tech event. Findings may not generalize across different contexts or communities.
