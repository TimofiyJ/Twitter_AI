from playwright.sync_api import sync_playwright
from ntscraper import Nitter
import pandas as pd


def scrape_single_tweet(url: str) -> dict:
    """
    Scrape a single tweet page for Tweet thread e.g.:
    https://twitter.com/Scrapfly_dev/status/1667013143904567296
    Return parent tweet, reply tweets and recommended tweets
    """
    _xhr_calls = []

    def intercept_response(response):
        """capture all background requests and save them"""
        # we can extract details from background requests
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # enable background request intercepting:
        page.on("response", intercept_response)
        # go to url and wait for the page to load
        page.goto(url)
        page.wait_for_selector("[data-testid='tweet']")

        # find all tweet background requests:
        tweet_calls = [f for f in _xhr_calls if "TweetResultByRestId" in f.url]
        for xhr in tweet_calls:
            data = xhr.json()
            return data['data']['tweetResult']['result']


def scrape_profile_tweets(username: str, number: int) -> pd.DataFrame:
    scraper = Nitter(log_level=1, skip_instance_check=False)
    tweets = scraper.get_tweets(username, mode="user", number=number)
    data = {
    'link':[],
    'text':[],
    'user':[],
    'likes':[],
    'quotes':[],
    'retweets':[],
    'comments':[]
    }

    for tweet in tweets['tweets']:
        data['link'].append(tweet['link'])
        data['text'].append(tweet['text'])
        data['user'].append(tweet['user']['name'])
        data['likes'].append(tweet['stats']['likes'])
        data['quotes'].append(tweet['stats']['quotes'])    
        data['retweets'].append(tweet['stats']['retweets'])    
        data['comments'].append(tweet['stats']['comments']) 

    df = pd.DataFrame(data)
    df.head()

    return df


if __name__ == "__main__":

    final_df = pd.DataFrame({"text"})
    usernames = ["taylorswift13", "StephenKing", "elonmusk", "KaiCenat", "BarackObama", "jimmyfallon", "badbanana", "limitlessmindon"]

    for username in usernames:
        tweets_df = scrape_profile_tweets(username, 10)
        final_df = pd.concat([final_df, tweets_df["text"]], ignore_index=True)

    final_df.to_csv("data.csv")
