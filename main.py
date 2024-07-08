import autogen
import os
from dotenv import load_dotenv
import config
import analyser_tools
import scrape

load_dotenv(override=True)

def main():
    

if __name__ == "__main__":
    config_list = {
        "model": config.model,
        "base_url": config.base_url,
        "api_key": os.getenv("GROQ_API_KEY"),
        "temperature": 0,
    }

    # manager_agent = autogen.UserProxyAgent(
    #         name="Manager_Agent",
    #         llm_config={"config_list": [config_list]},
    #         human_input_mode="NEVER",
    #         code_execution_config={"work_dir": "results", "use_docker": False},
    #         is_termination_msg=lambda msg: True
    #     )

    # analyser_agent = autogen.ConversableAgent(
    #         name="Analyser_agent",
    #         system_message="You are social media post analyser. You are given tweets \
    #             and additional information about them and you will need to improve their quality",
    #         llm_config={"config_list": [config_list]},
    #         code_execution_config=False,
    #         # max_consecutive_auto_reply=1,
    #         human_input_mode="NEVER",
    #     )
    username = str(input("Please, enter tweeter username for reference: "))
    tweets = scrape.scrape_profile_tweets(username, 5)
    # chat_results = manager_agent.initiate_chats(
    #     [
    #         {
    #             "recipient": analyser_agent,
    #             "message": f"What are the latest news in the {news_topic}?",
    #             "max_turns": 2,
    #             "clear_history": True,
    #         },
    #         {
    #             "recipient": parser_agent,
    #             "message": f"Use these URLs one by one to call your tool. The topic of the news: {news_topic}",
    #             "clear_history": True,
    #         },
    #         {
    #             "recipient": writer_agent,
    #             "message": f"Write newsletter from different news. The topic of the news: {news_topic}",
    #             "clear_history": True,
    #             "max_turns": 2,
    #         },
    #     ]
    # )
    instruction = analyser_tools.analyse_tool(tweets=tweets)

    tweet_example = "hello, dear subscribers, I want to share with you amazing news: we create new Youtube channel!"
    better_tweet = analyser_tools.write_tool(
        tweet=tweet_example,
        references=tweets["text"].tolist(),
        instruction=instruction
    )
    print(better_tweet)
