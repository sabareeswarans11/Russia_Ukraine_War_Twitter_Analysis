# Russia_Ukraine_War_Twitter_Analysis
Semi-Structured Data Processing with NoSQL Database Server MongoDB
Collecting Social Media Data from Twitter Real-time Data Stream and Storing and Retrieving to Process from a Semi-Structured Database Server MongoDB

# Project structure
 <details>
 <summary>In this project , there are 3 main files for 3 Takes :</summary>
 <summary>Task 1-Data collection: lab3_twitter/scrap_twitter_sab.py</summary>
  <p>-Automating scraping twitter API V2 using tweepy Python Package</p>
  <summary>Task 2- Data Storing: lab3_twitter/ MongoInsert_sab.py</summary>
  <p> -6k tweet text_data of JSON data is stored in MongoDb.</p>
  <summary>Task 3- Text Analysis : lab3_twitter/ TextAnalysis_EC.py</summary>
  <p> -With Wordnet help identified bigrams, trigrams and polysemy from stopword removed tokens.</p>
  <summary>Twitter data directory: Scraped data is stored as json and only the full Tweet Text is converted as CSV.</summary>
  <summary>Result directory:all the bigram.csv,Top10Words.csv, trigram.csv, and polysemy detection are stored
as CSV file.</summary>
        <summary>Config.ini: Twitter api key ,api token and secret for communicating with Twitter API v1 & v2 support.</summary>
          <summary>Requirements.text : all the frameworks , wordnet , header files used in this project information are
available.</summary>
   </details>

# My Twitter Developer Portal with API v1 and v2 support.
   <img width="452" alt="image" src="https://user-images.githubusercontent.com/94094997/159965945-41786534-851c-4844-bce1-1d393944c1f5.png">
I have requested for Elevated Access in twitter developer portal to scrap 6k User tweet based on topic : Russia_Ukraine_War 
