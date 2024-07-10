import streamlit as st
import pandas as pd
from ntscraper import Nitter
import analyser_tools
import scrape


def improve_tweet(username, tweet, number_of_tweets, max_length, old_tweet, topic):
    tweets = None

    if st.session_state['USERNAME'] != username or st.session_state['NUMBER_OF_TWEETS'] != number_of_tweets or 'TWEETS' not in st.session_state:
        st.session_state['USERNAME'] = username
        st.session_state['NUMBER_OF_TWEETS'] = number_of_tweets
        st.write(f"Scraping {username} tweets")
        tweets = scrape.scrape_profile_tweets(username, number=number_of_tweets)
        st.success(
                    f"Successfully scraped {number_of_tweets} tweets"
                )
        st.session_state.bool = False # Do not need to use old_tweet
        if 'TWEETS' not in st.session_state:
            st.session_state['TWEETS'] = tweets

    elif username == st.session_state['USERNAME'] and st.session_state['NUMBER_OF_TWEETS'] == number_of_tweets:
        tweets = st.session_state['TWEETS']
        st.session_state.bool = True # Need to use old_tweet comparison

    instruction = analyser_tools.analyse_tool(tweets=tweets)

    if st.session_state.bool is False:
        old_tweet = ""
    
    better_tweet = analyser_tools.write_tool(
            tweet=tweet,
            references=tweets["text"].tolist(),
            instruction=instruction,
            max_length=max_length,
            old_tweet = old_tweet,
            topic = topic
        )
    return better_tweet


# Streamlit app
st.title("Tweet improvement")
st.write("Enter a Twitter username to fetch recent tweets:")

username = st.text_input("Twitter Username", value="")
number_of_tweets = st.number_input(
    "Number of Tweets", min_value=1, max_value=10, value=5
)
max_length = st.number_input(
    "Maximum number of characters", min_value=1, max_value=4000, value=20
)

if 'NUMBER_OF_TWEETS' not in st.session_state:
    st.session_state['NUMBER_OF_TWEETS'] = number_of_tweets

if 'USERNAME' not in st.session_state:
    st.session_state['USERNAME'] = username

has_tweet = st.checkbox("I have tweet on my mind", value=False)

tweet = None
topic = None
if has_tweet:
    tweet = st.text_input("Enter your tweet", value="", key="tweet_input")
else:
    topic = st.text_input("Enter a topic for us to write tweet", value="", key="topic_input")

if st.button("Improve your tweet"):
    if tweet!=None or topic != None:
        with st.spinner("Improving the tweet"):
            try:
                if 'BETTER_TWEET' not in st.session_state:
                    better_tweet = improve_tweet(username, tweet, number_of_tweets, max_length, "", topic)
                else:
                    better_tweet = improve_tweet(username, tweet, number_of_tweets, max_length, st.session_state['BETTER_TWEET'],topic)
                st.success(
                    "Successfully improved tweet"
                )
                st.write(better_tweet)
                if 'BETTER_TWEET' not in st.session_state:
                    st.session_state['BETTER_TWEET'] = better_tweet
            except Exception as e:
                st.error(f"Error fetching tweets: {e}")
    else:
        st.error("Please enter tweet")