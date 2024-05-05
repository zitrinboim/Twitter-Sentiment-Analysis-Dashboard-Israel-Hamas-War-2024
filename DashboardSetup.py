import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import pymongo

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
tweets_db = mongo_client['tweets']
tweets_sentiments_collection = tweets_db['tweets_sentiments']
users_collection = tweets_db['users']

# Load data from MongoDB
pipeline = [
    {
        "$lookup": {
            "from": "users",
            "localField": "author_id",
            "foreignField": "id",
            "as": "authorDetails"
        }
    },
    {
        "$unwind": "$authorDetails"
    },
    {
        "$project": {
            "authorDetails.username": 1,
            "authorDetails.like_count": 1,
            "authorDetails.followers_count": 1,
            "authorDetails.location": 1,
            "created_at": 1,
            "id": 1,
            "like_count": 1,
            "reply_count": 1,
            "retweet_count": 1,
            "sentiment": 1,
        }
    }
]
result = list(tweets_sentiments_collection.aggregate(pipeline))
df = pd.DataFrame(result)

# Handle missing values
df['followers_count'] = df['authorDetails'].apply(lambda x: x.get('followers_count', None))
df.dropna(subset=['followers_count'], inplace=True)
df['username'] = df['authorDetails'].apply(lambda x: x.get('username', None))
df.dropna(subset=['username'], inplace=True)
df['location'] = df['authorDetails'].apply(lambda x: x.get('location', None))
df.dropna(subset=['location'], inplace=True)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(children=[
    html.H1(children='Twitter Sentiment Analysis Dashboard - Israel Hamas War 2024'),

    dcc.Graph(
        id='sentiment-pie-chart',
        figure=px.pie(df, names='sentiment', title='Sentiment Distribution')
    ),

    dcc.Graph(
        id='influencers-bar-chart',
        figure=px.bar(df.sort_values(by='followers_count', ascending=False).head(10),
                      x='username', y='followers_count',
                      title='Top Influencers')
    ),

    dcc.Graph(
        id='geographical-map',
        figure=px.scatter_geo(df.dropna(subset=['location']),
                              locations='location',
                              color='sentiment', title='Geographical Distribution')
    ),

    dcc.Graph(
        id='temporal-line-chart',
        figure=px.line(df.sort_values(by='created_at'),
                       x='created_at', y='sentiment',
                       title='Temporal Analysis')
    ),

    dcc.Graph(
        id='word-cloud',
        # Add your word cloud implementation here
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
