# russia_ukraine_war_twitter_analysis
Semi-Structured Data Processing with NoSQL Database Server MongoDB
Collecting Social Media Data from Twitter Real-time Data Stream and Storing and Retrieving to Process from a Semi-Structured Database Server MongoDB

# Project Structure
In this project , there are 3 main files for 3 Takes
1)Task 1-Data collection: lab3_twitter/scrap_twitter_sab.py
        -Automating scraping twitter API V2 using tweepy Python Package.
2)Task 2- Data Storing: lab3_twitter/ MongoInsert_sab.py
        -6k tweet text_data of JSON data is stored in MongoDb.
3)Task 3- Text Analysis : lab3_twitter/ TextAnalysis_EC.py
        -With Wordnet help identified bigrams, trigrams and polysemy from stopword removed tokens.
4)Twitter data directory: Scraped data is stored as json and only the full Tweet Text is converted as CSV.
5)Result directory:all the bigram.csv,Top10Words.csv, trigram.csv, and polysemy detection are stored
as CSV file.
6)Config.ini: Twitter api key ,api token and secret for communicating with Twitter API v1 & v2 support.
7)Requirements.text : all the frameworks , wordnet , header files used in this project information are
available.
