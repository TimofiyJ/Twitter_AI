import streamlit as st
import pandas as pd
from ntscraper import Nitter
import analyser_tools
import scrape


NUMBER_OF_TWEETS = 0
USERNAME = ""
TWEETS = 0

def improve_tweet(username, tweet, number_of_tweets):
    tweets = None
    if username == USERNAME and NUMBER_OF_TWEETS == number_of_tweets and TWEETS != 0:
        tweets = TWEETS
    else:
        tweets = scrape.scrape_profile_tweets(username, number=number_of_tweets)
        TWEETS = tweets

    instruction = analyser_tools.analyse_tool(tweets=tweets)

    better_tweet = analyser_tools.write_tool(
        tweet=tweet,
        references=tweets["text"].tolist(),
        instruction=instruction
    )
    return better_tweet

if __name__ == "__main__":
    better_tweet = improve_tweet("elonmusk","Hello! Happy to anounce we launch our new youtube channel", 5)
    print(better_tweet)