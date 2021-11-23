

import tweepy
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List
from tweepy import api
from config import consumer_key, consumer_secret

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)


def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    for tweet in tweepy.Cursor (api.search_tweets, q=keyword, tweet_mode="extended", lang="en").items(10):
        all_tweets.append(tweet.full_text)

    return all_tweets


def clean_tweets(all_tweets: List[str]) -> List[str]:
    tweets_clean = []
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))

    return tweets_clean


def get_sentiment(all_tweets: List[str]) -> List[float]:
    sentiment_scores = []
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)

    return sentiment_scores


def generate_average_sentiment_score(keyword: str) -> int:
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)

    average_score = statistics.mean(sentiment_scores)

    return average_score


if __name__ == "__main__":

    print("what does the people prefer?  ")
    first_product = input()
    print("... or ....")
    second_product = input()
    print("\n")

    first_score = generate_average_sentiment_score(first_product)
    second_score = generate_average_sentiment_score(second_product)

    if (first_score > second_score):
        print(f"People prefers {first_product} over {second_product}!")
    else:
        print(f"People prefers {second_product} over {first_product}!")

    print(first_score)
    print(second_score)
   