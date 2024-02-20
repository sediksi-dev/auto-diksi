from dotenv import load_dotenv
from helper.md_prompt import prompt_from_md

from langchain_openai import ChatOpenAI
from langchain.output_parsers import JsonOutputKeyToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from .models import CreateOutlineFromArticleArgs, OutlineArticle

load_dotenv()


@tool
def outline_generator(
    outline: OutlineArticle,
) -> OutlineArticle:
    """Extract the important points from the original article and organize them into an article structure consisting of intro, sections, and further insights."""
    return outline


def create_outline_from_article(args: CreateOutlineFromArticleArgs) -> OutlineArticle:
    """
    To create an outline for the article, we need to analyze the original article and the writing guidelines.
    1. We will use the original article to create a system prompt.
    2. We will use the writing guidelines to create a human prompt.
    3. We will use the system and human prompts to analyze the outline.
    4. We will use the analysis to create the outline.
    5. We will return the outline.

    Args:
    - original_article (str): The original article. This is the article that we want to create an outline for.
    - lang_target (str): The target language for the article. Default is "indonesia".
    - lang_source (str): The source language for the article. Default is "english".
    """

    # Define the configuration for the OpenAI model
    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }

    # Get the system and human prompts for the analysis. The prompts are provided in markdown files and necessary variables are passed to the prompts.
    system_prompt = prompt_from_md(
        "modules/ai/tasks/create_outline/prompts/system.md",
        lang_target=args.lang_target,
        lang_source=args.lang_source,
    )
    human_prompt = prompt_from_md(
        "modules/ai/tasks/create_outline/prompts/human.md",
        original_article=args.original_article,
        lang_target=args.lang_target,
    )

    # Initializing the model
    llm = ChatOpenAI(**openai_config)
    model = llm.bind_tools(tools=[outline_generator], tool_choice="outline_generator")
    prompts = ChatPromptTemplate.from_messages(
        [("system", "{system_prompt}"), ("human", "{human_prompt}")]
    )

    # Defining the pipeline for analyzing the outline
    generate_topics_and_facts = (
        prompts
        | model
        | JsonOutputKeyToolsParser(key_name="outline_generator", return_single=True)
    )

    # Analyzing the outline
    response = generate_topics_and_facts.invoke(
        {
            "system_prompt": system_prompt,
            "human_prompt": human_prompt,
        }
    )

    try:
        response = OutlineArticle(**response["outline"])
        return response
    except Exception as e:
        raise e
