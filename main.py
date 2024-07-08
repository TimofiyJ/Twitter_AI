import streamlit as st
import pandas as pd
from ntscraper import Nitter
import analyser_tools
import scrape


def improve_tweet(username, tweet, number_of_tweets):
    tweets = None
    if st.session_state['USERNAME'] != username or st.session_state['NUMBER_OF_TWEETS'] != number_of_tweets or 'TWEETS' not in st.session_state:
        st.session_state['USERNAME'] = username 
        st.session_state['NUMBER_OF_TWEETS'] = number_of_tweets
        st.write(f"Scraping {username} tweets")
        tweets = scrape.scrape_profile_tweets(username, number=number_of_tweets)
        st.success(
                    f"Successfully scraped {number_of_tweets} tweets"
                )
        if 'TWEETS' not in st.session_state:
            st.session_state['TWEETS'] = tweets

    if username == st.session_state['USERNAME'] and st.session_state['NUMBER_OF_TWEETS'] == number_of_tweets:
        tweets = st.session_state['TWEETS']

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