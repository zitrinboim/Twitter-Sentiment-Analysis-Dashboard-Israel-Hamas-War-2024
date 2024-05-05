# Sentiment Analysis - Twitter - Israel Hamas War - 2024

## Project Description:
This project focuses on sentiment analysis of tweets related to the Israel-Hamas conflict on Twitter. It involves analyzing the sentiment of tweets mentioning either Israel or Hamas and organizing the data based on various parameters such as followers, geographic location, timing, and frequency of positive or negative tweets. The project presents this analyzed data in a dashboard using Plotly and Dash libraries, allowing users to visualize and understand sentiment trends.

## Installation Instructions:
To run this project, follow these steps:
1. Install Python if you haven't already.
2. Clone this repository to your local machine.
3. Install the required Python libraries using pip:
   ```
   pip install plotly dash openai numpy pandas pymongo
   ```
4. Obtain Twitter and OpenAI API keys (for a fee) and configure them in the project.

## Usage Instructions:
1. Run the Python script to collect tweets, analyze sentiment, and store data in MongoDB.
2. Start the dashboard using Dash to visualize sentiment analysis results.
3. Explore the dashboard to gain insights into sentiment trends related to the Israel-Hamas conflict.

## Features:
- Collects tweets mentioning Israel or Hamas from Twitter API.
- Analyzes sentiment using OpenAI's GPT API.
- Stores analyzed data in MongoDB.
- Presents sentiment analysis results in an interactive dashboard using Plotly and Dash.

## Examples from the dashboard
![צילום מסך 2024-05-05 105334](https://github.com/zitrinboim/Twitter_Sentiment_Analysis_Dashboard_Israel_Hamas_War_2024/assets/91831329/deead9e5-6e68-43d5-9522-37bd36b830ee)
![newplot (4)](https://github.com/zitrinboim/Twitter_Sentiment_Analysis_Dashboard_Israel_Hamas_War_2024/assets/91831329/2f25499d-daea-4bb6-9b82-c65ed65f51a9)
![newplot](https://github.com/zitrinboim/Twitter_Sentiment_Analysis_Dashboard_Israel_Hamas_War_2024/assets/91831329/e5d88e5a-dd54-4f38-a98b-29925c39caf8)

## Dependencies:
- plotly
- dash
- openai
- numpy
- pandas
- pymongo

## Additional Information:
- This project requires Twitter and OpenAI API keys (for a fee).
- Ensure that you comply with Twitter's API usage policy and any relevant legal requirements while collecting and analyzing tweets.
- Make sure to handle sensitive data, such as API keys, securely to prevent unauthorized access.

**Disclaimer:** This project is for educational and research purposes only. The sentiment analysis results may not reflect the opinions or views of individuals accurately. Use the information provided with discretion.

