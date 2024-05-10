import subprocess
import os

from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool

load_dotenv()
llm = OpenAI()


def write_haiku(topic: str) -> str:
    """
    Write a haiku about a given topic
    """
    return llm.complete(f"write me a haiku about {topic}")


def count_characters(text: str) -> str:
    """
    Counts the number of characters in a text
    """
    return len(text)


def open_application(application_name: str) -> str:
    """
    Opens an application in my computer
    """

    try:
        subprocess.Popen(["/usr/bin/open", "-n", "-a", application_name])
        return "successfully opened application"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "failed to open application"


def open_url(url: str) -> str:
    """
    Opens a url in browser (chrome/safari/firefox)
    """
    try:
        subprocess.Popen(["/usr/bin/open", "--url", url])
        return "Succesfully opened url"
    except Exception as e:
        return "failed to open application"


if __name__ == "__main__":
    print("Hello agents llamaIndex")

    tool1 = FunctionTool.from_defaults(
        fn=write_haiku,
        name="write_haiku",
        description=" Writes a Haiku about a given topic",
    )
    tool2 = FunctionTool.from_defaults(
        count_characters,
        name="count_characters",
        description="Useful to count the number of characters in a text",
    )
    tool3 = FunctionTool.from_defaults(
        open_application,
        name="open_application",
        description="Opens an application on my computer",
    )

    tool4 = FunctionTool.from_defaults(
        open_url,
        name="open_url",
        description="Opens a url on my computer",
    )
    agent = ReActAgent.from_tools(
        tools=[tool1, tool2, tool3, tool4], llm=llm, verbose=True
    )

    # res = agent.query(
    #     "Write a haiku about cheating and then count the characters in it"
    # )
    res = agent.query("Write a Haiku about Jesus and then count the characters and then open youtube.com")
    print(res)
