import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import pymongo
import determiningSentiment
# Sets DB details
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client['tweets']
tweetsCollection = db['tweets_sentiments']
usersCollection = db['users']
# Get the current time in local time & Set timezone to UTC
current_time_utc = datetime.now().replace(tzinfo=timezone.utc)
# Subtract one week from the current date
new_time = current_time_utc - timedelta(weeks=1)
# Convert the time to the desired format with three digits after the period
formatted_time = new_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKLlrAEAAAAAfySht%2F8LsDAk5vNZsXuKsgsBdvI%3DIFuVNSjVC8ZFVpivVLjR00g20ZjEBLaPt7iyX1iWBiulew6Kya"
search_url = "https://api.twitter.com/2/tweets/search/recent"
query_params = {'query': '(Israel OR IDF -is:retweet)', 'max_results': '50',
                'tweet.fields': 'author_id,geo,created_at,note_tweet,public_metrics',
                'place.fields': 'full_name,country,geo',
                'user.fields': 'id,name,location,public_metrics',
                'expansions': 'author_id'}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# The Tweets will be made into a data frame using the following code:
def make_df(response):
    return pd.DataFrame(response['data'])


def send_to_mongo_db(json_response):
    json_response_data = json_response['data']
    for item in json_response_data:
        existing_record = tweetsCollection.find_one({"_id": item['id']})
        if not existing_record:
            public_metrics = item['public_metrics']
            document = {
                'author_id': item['author_id'],
                'created_at': item['created_at'],
                'id': item['id'],
                'like_count': public_metrics['like_count'],
                'reply_count': public_metrics['reply_count'],
                'bookmark_count': public_metrics['bookmark_count'],
                'impression_count': public_metrics['impression_count'],
                'quote_count': public_metrics['quote_count'],
                'retweet_count': public_metrics['retweet_count'],
                'sentiment': determiningSentiment.sentiment(item['text']),
                'text': item['text']
            }
            tweetsCollection.insert_one(document)
    json_response_users = json_response['includes']['users']
    for item in json_response_users:
        existing_record = usersCollection.find_one({"_id": item['id']})
        if not existing_record:
            public_metrics = item['public_metrics']
            document = {
                'name': item['name'],
                'username': item['username'],
                'id': item['id'],
                'like_count': public_metrics['like_count'],
                'followers_count': public_metrics['followers_count'],
                'following_count': public_metrics['following_count'],
                'listed_count': public_metrics['listed_count'],
                'tweet_count': public_metrics['tweet_count'],
            }
            try:
                document['location'] = item['location']
            except KeyError:
                document['location'] = "None"
            usersCollection.insert_one(document)


def main():
    json_response = connect_to_endpoint(search_url, query_params)
    send_to_mongo_db(json_response)


if __name__ == "__main__":
    main()
