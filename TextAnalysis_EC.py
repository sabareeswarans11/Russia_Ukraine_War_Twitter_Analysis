"""
coding:utf-8
SPRING 2022 -CIS 493/593 – BIG DATA LAB ASSIGNMENT - 3
Author: Sabareeswaran Shanmugam
steps:
1)Basic cleaning: emoji , Hashtag removal
2)stop word removal
3) Top 10 words after Stopword removal
4) Extra -credit part - detected bigrams,trigrams and polysemy in tokens
"""
import string

import matplotlib.pyplot as plt

string.punctuation
import os
import preprocessor as p # This package is helpful in cleaning ( Removing emoji #Hastags ) tweet-preprocessor // pip3 install tweet-preprocessor.
import nltk
import csv
import numpy as np
from nltk.corpus import wordnet as wn
import string
import re
import ssl
from textblob import TextBlob
import seaborn as sns
from wordcloud import WordCloud
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
#nltk.download('all')
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import pandas as pd

# Set Absolute_path to ROOT.
sab_absolute_path = os.path.dirname(os.path.abspath(__file__))

def stopword_removal_tweet(text):
    sw=stopwords.words('english')
    # user defined stopwords is added to the NLTK stopwords based on real-time Twitter tweets.
    sw.extend(['the','va','wa','ha','i','we','ve','le','u','hi','...',"i've","i'm","we've",'im','):','w','ian'])
    words = [word for word in text.split(" ") if word.lower() not in sw]
    words = list(filter(len,words))
    #print("Text Tweets after removing stopwords:", words)
    return words

def generate_N_grams(Wordlist,ngram):
  temp=zip(*[Wordlist[i:] for i in range(0,ngram)])
  result=[' '.join(ngram) for ngram in temp]
  return result

def lemmatize_text(text):
    return [(lemmatizer.lemmatize(w)) for w in w_tokenizer.tokenize(text)]

def remove_punctuation(text):
    exceptional=['...','..']
    if(type(text)==float):
        return text
    preprocessed=""
    for elt in text:
        if elt not in string.punctuation and exceptional:
            preprocessed=preprocessed+' '+elt
            preprocessed_result= preprocessed.replace('...','')
    return preprocessed_result.lower().replace(':/','')

def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1
if __name__ == "__main__":

    # Processing the big 6k data in dataframe for ease of visualization.
    ukraine_tweets =pd.read_csv(sab_absolute_path + '/twitter_data/UkraineTextData6k_Sab.csv',sep='\t',names=['Tweet_Text'])

    ukraine_tweets['Extract hashtag'] = ukraine_tweets['Tweet_Text'].apply(lambda x: re.findall(r"#(\w+)", x))
    print(ukraine_tweets['Extract hashtag'])
    # cleaning the data
    for i, v in enumerate(ukraine_tweets['Tweet_Text']):
        ukraine_tweets.loc[i,'Cleaned_Tweet_Text'] = p.clean(v)

    # Removing Numbers - cleaning stage.
    ukraine_tweets['Numbers_Removed_Text']=ukraine_tweets['Cleaned_Tweet_Text'].str.replace('\d+', '')

    # Extracting Keywords (Here lemmatization performs better than Stemming.)
    lemmatizer = nltk.stem.WordNetLemmatizer()
    w_tokenizer = TweetTokenizer()
    ukraine_tweets['Text_lemmatize']= ukraine_tweets['Numbers_Removed_Text'].apply(lemmatize_text)

    # punctuation removal.
    ukraine_tweets['PreProcessed_Tweet_text']= ukraine_tweets['Text_lemmatize'].apply(lambda x:remove_punctuation(x))

    # Stopword Removal
    ukraine_tweets['StopwordRemoval_tweets'] =ukraine_tweets['PreProcessed_Tweet_text'].apply(stopword_removal_tweet)

    # Preprocessed Tweet Text
    print("PreProcessed_Tweet_Text_Before_Stop_Word_Removal")
    print(ukraine_tweets['PreProcessed_Tweet_text'])
    # Stopword Removed Dataframe
    print("Stop_Word_Removed_Tweet_Text_dataframe")
    print(ukraine_tweets['StopwordRemoval_tweets'])

    # making all different tweet message flatten into a single list.
    all_together = ukraine_tweets['StopwordRemoval_tweets'].values.tolist()
    flat_list = [item for sublist in all_together for item in sublist]
    removetable = str.maketrans('','','...')
    # making all different tweet message flatten into a single list.
    flatten_list =[s.translate(removetable) for s in flat_list]
    #print(flatten_list)
    df5 = pd.DataFrame(flatten_list)
    # storing Stopword removed tokens in CSV file for polysemy detection.
    df5.to_csv(sab_absolute_path + '/Results/Stopword.csv', index=False)
    sw1 = stopwords.words('english')
    sw1.extend(['the', 'va', 'wa', 'ha', 'i','we','ve', 'u'])

    # Top 10 Words Detection with frequency after Stopword Removal.
    matchfound = []
    for wds in flatten_list:
        if wds.lower() not in sw1 and wds not in matchfound:
            matchfound.append(wds)
        # Make a list of (count, unique words) tuples.
    frequency = []
    for exactmatch in matchfound:
        frequency_count = 0
        for word in flatten_list:
            if word == exactmatch:
                frequency_count += 1
        frequency.append((frequency_count, exactmatch))

    frequency.sort()  # Sorting the list makes lowest counts first.
    frequency.reverse()  # Reverse it, makes largest counts first.

    #Top 10 Words Detection and printing in console
    Top_10_frequency=[]
    # Print the ten words with the highest counts.
    print("Top 10 Frequency tokens:")
    print("Words and their Frequency(Count)")
    for i in range(min(10,len(frequency))):
        count, word = frequency[i]
        Top_10_frequency.append((count,word))
        print('%s %d' % (word, count))
    df4 = pd.DataFrame(Top_10_frequency)
    df4.to_csv(sab_absolute_path + '/Results/Top10Words.csv', header=["Frequency","Words"], index=False)
    # Started Processing bigram,trigram and polysemy Detection
    # Bigram Detection
    print("Processing bigram Detection :)")
    bigram_result=generate_N_grams(flatten_list,2)
    df = pd.DataFrame(bigram_result)
    df.to_csv(sab_absolute_path+'/Results/bigram.csv',header=["Bigram-2 Words"], index=False)
    #print(bigram_result)
    # Trigram Detection
    print("Processing Trigram Detection :)")
    trigram=generate_N_grams(flatten_list,3)
    df2 = pd.DataFrame(trigram)
    df2.to_csv(sab_absolute_path + '/Results/trigram.csv',header=["Trigram 3 Words"], index=False)
    #print(trigram)

    #polysemy Detection
    # Logic: Used WORDNET Dictionary to detect Polysemy in the preprocessed tokens
    # import stopword removed tokens from the generated csv.
    print("Processing Polysemy Detection :)")
    poly = csv.reader(open(sab_absolute_path + '/Results/Stopword.csv'))
    #Flatten list of list into single list.
    flatten_set_for_polysemy = []
    for line in poly:
        seperator = '[]'
        flatten_set_for_polysemy.append(seperator.join(line))
    #print(flatten_set_for_polysemy)

    polysemy_detection_in_stopwordRemoved_tokens = []
    polysemy_dectected_token = []

    for i in flatten_set_for_polysemy:
        s = i
        for syn in wn.synsets(str(s)):
        # if search word has more than one lemma( synomnys) it means the word has 2 different meaning i.e polysemy.
            if len(tuple(syn.lemma_names())) > 1:
                string = 'Polysemy'
                polysemy_dectected_token.append((str(s)))
            else:
                string = 'Not a Polysemy'
            polysemy_detection_in_stopwordRemoved_tokens.append((str(s), tuple(syn.lemma_names()), string, syn.definition(), syn.name()))

    # Storing all the Processed text analysis as CSV file for future works.
    poly_df2 = pd.DataFrame(set(polysemy_detection_in_stopwordRemoved_tokens))
    poly_df2.to_csv(sab_absolute_path + '/Results/polysemydetection_StopwordRemoved_tokens.csv',
               header=["Extracted word after stopword", "Different Meaning", "Detection", "Definition of the token",
                       "Dictionary-NLTK-wordnet"], index=False)
    poly_df3 = pd.DataFrame(set(polysemy_dectected_token))
    poly_df3.index =np.arange(1,len(poly_df3)+1)
    poly_df3.to_csv(sab_absolute_path + '/Results/polydetected_tokens.csv',
               header=["Polysemy Detected words based on Wordnet "], index_label='No of words')
    print("Total No of Polysemy words:", len(poly_df3))
    print("Total No of Extracted tokens after Preprocessing words:", len(poly_df2))
    print('Bigram ,Trigram ,Polysemy extracted to Results Directory :)')
    print('Sentimental Analysis processing...')
    # sentimental analysis
    ukraine_tweets['Sentiment'] = ukraine_tweets['PreProcessed_Tweet_text'].apply(lambda x: analyze_sentiment(x))
    ukraine_tweets['Length'] = ukraine_tweets['PreProcessed_Tweet_text'].apply(len)
    ukraine_tweets['Word_counts'] = ukraine_tweets['PreProcessed_Tweet_text'].apply(lambda x: len(str(x).split()))
    SentimentalAnalysis = ukraine_tweets[['PreProcessed_Tweet_text', 'Length', 'Sentiment', 'Word_counts']]
    sentiment = ukraine_tweets['Sentiment'].value_counts()
    fig = plt.figure(figsize=(15, 15))
    ax = sns.countplot(data=SentimentalAnalysis, x='Sentiment')
    fig.savefig(sab_absolute_path + '/Results/Sentimental_Analysis/Bargraph_Sentiment_Analysis.png')

    fig, ax = plt.subplots(figsize=(6, 6))
    sizes = [count for count in ukraine_tweets['Sentiment'].value_counts()]
    labels = list(ukraine_tweets['Sentiment'].value_counts().index)
    explode = (0.1, 0, 0)
    ax.pie(x=sizes, labels=labels, autopct='%1.1f%%', explode=explode)
    ax.set_title('Sentimental Analysis of Russia ukraine war', fontsize=15)
    fig.savefig(sab_absolute_path + '/Results/Sentimental_Analysis/Piechart_Sentiment_Analysis.png')

    neutral_tweets = ukraine_tweets[ukraine_tweets['Sentiment'] == 0]
    positive_tweets = ukraine_tweets[ukraine_tweets['Sentiment'] == 1]
    negative_tweets = ukraine_tweets[ukraine_tweets['Sentiment'] == -1]

    print("Neutral tweet example :", neutral_tweets['PreProcessed_Tweet_text'].values[11])
    neutral_tweets['PreProcessed_Tweet_text'].to_csv(sab_absolute_path + '/Results/Sentimental_Analysis/Neutral_tweets.csv',
                                                     header=["Neutral Tweets"], index=False)
    print("Positive Tweet example :", positive_tweets['PreProcessed_Tweet_text'].values[12])
    positive_tweets['PreProcessed_Tweet_text'].to_csv(sab_absolute_path + '/Results/Sentimental_Analysis/Positive_tweets.csv',
                                                      header=["Positive Tweets"], index=False)
    print("Negative Tweet example :", negative_tweets['PreProcessed_Tweet_text'].values[40])
    negative_tweets['PreProcessed_Tweet_text'].to_csv(sab_absolute_path + '/Results/Sentimental_Analysis/Negative_tweets.csv',
                                                      header=["Negative Tweets"], index=False)

    cleantxt = ' '.join(text for text in ukraine_tweets['PreProcessed_Tweet_text'])
    wordcloud = WordCloud(background_color='black', random_state=11, max_font_size=100, max_words=150, width=1000,
                          height=1000).generate(cleantxt)
    fig = plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Cleaned Text Tweets', loc='center')
    fig.savefig(sab_absolute_path + '/Results/Sentimental_Analysis/CleanText_wordcloud.png')

    positive_words = ' '.join(
        [text for text in ukraine_tweets['PreProcessed_Tweet_text'][ukraine_tweets['Sentiment'] == 1]])
    wordcloud = WordCloud(background_color='green', width=1000, height=1000, random_state=11,
                          max_font_size=110).generate(positive_words)
    fig = plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.title('Positive Text Tweets', loc='center')
    fig.savefig(sab_absolute_path + '/Results/Sentimental_Analysis/Positive_wordcloud.png')

    negative_words = ' '.join(
        [text for text in ukraine_tweets['PreProcessed_Tweet_text'][ukraine_tweets['Sentiment'] == -1]])
    wordcloud = WordCloud(background_color='blue', width=1000, height=1000, random_state=11, max_font_size=110,
                          max_words=150).generate(negative_words)
    fig = plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.title('Negative Text Tweets', loc='center')
    fig.savefig(sab_absolute_path + '/Results/Sentimental_Analysis/negative_wordcloud.png')

    neutral_words = ' '.join(
        [text for text in ukraine_tweets['PreProcessed_Tweet_text'][ukraine_tweets['Sentiment'] == 0]])
    wordcloud = WordCloud(background_color='orange', width=1000, height=1000, random_state=11,
                          max_font_size=110).generate(neutral_words)
    fig = plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.title('Neutral Text Tweets', loc='center')
    fig.savefig(sab_absolute_path + '/Results/Sentimental_Analysis/Neutral_wordcloud.png')
    print('Sentimental Results  were stored under Results/Sentimental_Analysis/ directory :)')
    print('Program end !')



'''
Reference:
1)https://stackoverflow.com/questions/22006286/how-to-find-polysemy-words-from-input-query
2)https://stackoverflow.com/questions/33536022/how-can-i-print-the-entire-contents-of-wordnet-preferably-with-nltk
3)https://towardsdatascience.com/text-analysis-basics-in-python-443282942ec5
4)https://stackoverflow.com/questions/24347029/python-nltk-bigrams-trigrams-fourgrams
'''
