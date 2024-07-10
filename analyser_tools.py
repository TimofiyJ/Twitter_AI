from typing_extensions import Annotated, List
import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import config
from pandas import DataFrame

load_dotenv()


def write_tool(
    tweet,
    references: Annotated[List[str], "List of references for the writing style"],
    instruction: Annotated[str, "Instruction to fit in a style format"],
    max_length: Annotated[int, "Maximum number of characters for the tweet"],
    old_tweet: Annotated[str, "Old suggestion by model"],
    topic: Annotated[str, "Topic for a tweet"],
) -> str:
    """Tool for the Analyser Agent to write social media post
    based on provided style
     Args:
        tweet (str): user initial text

    Returns:
        str: new text for social media post based on provided style
    """
    llm = ChatGroq(
        model=config.model,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=config.temperature,
    )
    tweet_references = ""
    for i in range(len(references)):
        tweet_references = (
            tweet_references + f"Reference tweet #{i+1}" + "\n" + references[i] + "\n"
        )

    base_prompt = None
    llm_result = None

    if tweet is not None:
        base_prompt = PromptTemplate(
            template="""You are provided with tweet examples and instruction to fit in these tweet's style.
            References: {references}
            Instruction: {instruction}
            Text: {text}
            Do not do text longer than {max_length} characters""",
            input_variables=["references", "instruction", "text", "max_length", "old_tweet"],
        )
        chain = base_prompt | llm
        llm_result = chain.invoke(
            {
                "references": tweet_references,
                "instruction": instruction,
                "text": tweet,
                "max_length": max_length,
                "old_tweet": old_tweet
            }
        )
    else:
        base_prompt = PromptTemplate(
            template="""You are provided with tweet examples and instruction to fit in these tweet's style.
            You are also provided with topic so you create tweet based on this topic
            References: {references}
            Instruction: {instruction}
            Topic: {text}
            Do not do text longer than {max_length} characters""",
            input_variables=["references", "instruction", "text", "max_length", "old_tweet"],
        )
        chain = base_prompt | llm
        llm_result = chain.invoke(
            {
                "references": tweet_references,
                "instruction": instruction,
                "text": topic,
                "max_length": max_length,
                "old_tweet": old_tweet
            }
        )

    return str(llm_result.content)


def analyse_tool(
    tweets: Annotated[DataFrame, "List of references for the writing style"],
) -> str:
    """Tool for the Analyser Agent to analyse the best tweets and generate
    reasoning why they are popular and provide instructions how to
    create tweets with similar style
     Args:
        tweets (List[str]): tweets of a particular user

    Returns:
        str: instruction how to create tweets with similar style
    """
    llm = ChatGroq(
        model=config.model,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=config.temperature,
    )
    tweet_examples = ""
    for i in range(len(tweets)):
        tweet_examples = (
            tweet_examples + f"Tweet #{i+1}" + "\n Text:" + tweets.iloc[i]["text"]
        )
        tweet_examples = (
            tweet_examples
            + f"\n Statistics: likes {tweets.iloc[i]['likes']}; comments {tweets.iloc[i]['comments']}"
        )
        tweet_examples = (
            tweet_examples
            + f"quotes {tweets.iloc[i]['quotes']}; retweets {tweets.iloc[i]['retweets']}"
        )

    base_prompt = PromptTemplate(
        template="""You are provided with user tweets and their statistics. Find the similarities or special style
        between these tweets and analyse the most popular of them. Your answer is to generate instruction that helps create 
        tweets with similar style.
        {tweets}""",
        input_variables=["tweets"],
    )

    chain = base_prompt | llm
    llm_result = chain.invoke({"tweets": tweet_examples})

    return str(llm_result.content)
