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

    if st.session_state['USERNAME'] != username or st.session_state['NUMBER_OF_TWEETS'] != number_of_tweets or 'TWEETS' not in st.session_state:
        st.session_state['USERNAME'] = username 
        st.session_state['NUMBER_OF_TWEETS'] = number_of_tweets
        tweets = scrape.scrape_profile_tweets(username, number=number_of_tweets)
        if 'TWEETS' not in st.session_state:
            st.session_state['TWEETS'] = tweets

    if username == USERNAME and NUMBER_OF_TWEETS == number_of_tweets:
        tweets = st.session_state['TWEETS']

    instruction = analyser_tools.analyse_tool(tweets=tweets)

    better_tweet = analyser_tools.write_tool(
        tweet=tweet,
        references=tweets["text"].tolist(),
        instruction=instruction
    )
    return better_tweet


# Streamlit app
st.title("Tweet improvement")
st.write("Enter a Twitter username to fetch recent tweets:")

username = st.text_input("Twitter Username", value="")
number_of_tweets = st.number_input(
    "Number of Tweets", min_value=1, max_value=10, value=5
)

if 'NUMBER_OF_TWEETS' not in st.session_state:
    st.session_state['NUMBER_OF_TWEETS'] = number_of_tweets

if 'USERNAME' not in st.session_state:
    st.session_state['USERNAME'] = username

tweet = st.text_input("Enter your tweet", value="")
if st.button("Improve your tweet"):
    if tweet:
        with st.spinner("Improving the tweet"):
            try:
                better_tweet = improve_tweet(username, tweet, number_of_tweets)
                st.success(
                    "Successfully improved tweet"
                )
                st.write(better_tweet)
            except Exception as e:
                st.error(f"Error fetching tweets: {e}")
    else:
        st.error("Please enter tweet")