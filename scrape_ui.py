import streamlit as st
import pandas as pd
from playwright.sync_api import sync_playwright
from ntscraper import Nitter


# Function to scrape profile tweets
def scrape_profile_tweets(username: str, number: int) -> pd.DataFrame:
    st.write("Setting up the environment")
    scraper = Nitter(log_level=1, skip_instance_check=False)
    st.write("The environment was setted up")
    tweets = scraper.get_tweets(username, mode="user", number=number)
    data = {
        "link": [],
        "text": [],
        "user": [],
        "likes": [],
        "quotes": [],
        "retweets": [],
        "comments": [],
    }

    for tweet in tweets["tweets"]:
        data["link"].append(tweet["link"])
        data["text"].append(tweet["text"])
        data["user"].append(tweet["user"]["name"])
        data["likes"].append(tweet["stats"]["likes"])
        data["quotes"].append(tweet["stats"]["quotes"])
        data["retweets"].append(tweet["stats"]["retweets"])
        data["comments"].append(tweet["stats"]["comments"])

    df = pd.DataFrame(data)
    return df


# Streamlit app
st.title("Twitter Profile Scraper")
st.write("Enter a Twitter username to fetch recent tweets:")

username = st.text_input("Twitter Username", value="")
number_of_tweets = st.number_input(
    "Number of Tweets", min_value=1, max_value=10, value=5
)

if st.button("Fetch Tweets"):
    if username:
        with st.spinner(f"Fetching {number_of_tweets} tweets for @{username}..."):
            try:
                tweets_df = scrape_profile_tweets(username, number_of_tweets)
                st.success(
                    f"Successfully fetched {number_of_tweets} tweets for @{username}"
                )
                st.write(tweets_df)
            except Exception as e:
                st.error(f"Error fetching tweets: {e}")
    else:
        st.error("Please enter a valid Twitter username.")

st.write("Enter your tweet:")

tweet = st.text_input("Tweet", value="")
if st.button("Improve your tweet"):
    if tweet:
        with st.spinner("Improving the tweet"):
            try:
                tweets_df = scrape_profile_tweets(username, number_of_tweets)
                st.success(
                    f"Successfully fetched {number_of_tweets} tweets for @{username}"
                )
                st.write(tweets_df)
            except Exception as e:
                st.error(f"Error fetching tweets: {e}")
    else:
        st.error("Please enter a valid Twitter username.")