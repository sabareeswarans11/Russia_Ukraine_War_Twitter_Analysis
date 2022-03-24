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

<img width="1914" alt="Screenshot 2022-03-23 at 11 22 15 PM" src="https://user-images.githubusercontent.com/94094997/159966469-2e0b5d46-acd1-4411-b04c-6f891613f44e.png">


I have requested for Elevated Access in twitter developer portal to scrap 6k User tweet based on topic : Russia_Ukraine_War 

# MongoDb Compass (GUI Support to Process and visualize the JSON semi-formatted twitter data)

<img width="1460" alt="Screenshot 2022-03-23 at 11 41 26 PM" src="https://user-images.githubusercontent.com/94094997/159966684-263fa497-6f79-42ea-99c3-e6d5900e6ec3.png">
<img width="1501" alt="Screenshot 2022-03-23 at 11 47 46 PM" src="https://user-images.githubusercontent.com/94094997/159967848-1431bc35-e72a-4a9c-91b4-613256cc2e0f.png">

# Result Top 10 Most frequent topic words
<img width="974" alt="Screenshot 2022-03-24 at 1 37 46 AM" src="https://user-images.githubusercontent.com/94094997/159967917-0f709b2a-2bfc-4bce-aa82-5fc8d133c535.png">

# Result: Bi-gram Detection
<img width="1224" alt="Screenshot 2022-03-24 at 1 37 04 AM" src="https://user-images.githubusercontent.com/94094997/159968074-f9c6e76e-1075-4cb2-852b-117b7f1df46f.png">


# Result: Tri-gram Detection

<img width="974" alt="Screenshot 2022-03-24 at 1 37 46 AM" src="https://user-images.githubusercontent.com/94094997/159968165-2b3390f7-f62b-4ed8-869c-2471746e6e3f.png">




