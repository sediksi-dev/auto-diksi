from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from helper.md_prompt import prompt_from_md
from .models import CreateIntroArgs

load_dotenv()


def create_intro(args: CreateIntroArgs) -> str:
    """
    To create an introduction for the article, we need to analyze the SEO data and the writing guidelines.
    1. We will use the SEO data to create a system prompt.
    2. We will use the writing guidelines to create a human prompt.
    3. We will use the system and human prompts to analyze the outline.
    4. We will use the analysis to create the introduction.
    5. We will return the introduction.
    """

    # Define the configuration for the OpenAI model
    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }

    system_prompt = prompt_from_md(
        "modules/ai/tasks/create_intro/prompts/system.md",
        lang_target=args.lang_target,
        keyword=args.keyword,
        title=args.title,
        description=args.description,
        intent=args.intent,
        style=args.style,
        tone=args.tone,
    )

    human_prompts = prompt_from_md(
        "modules/ai/tasks/create_intro/prompts/human.md",
        intro_guideline=args.intro_guideline,
        lang_target=args.lang_target,
    )

    # Initializing the model
    model = ChatOpenAI(**openai_config)

    prompts = ChatPromptTemplate.from_messages(
        [("system", "{system_prompt}"), ("human", "{human_prompt}")]
    )

    # Defining the pipeline for analyzing the outline
    analysis_seo = prompts | model

    response = analysis_seo.invoke(
        {
            "system_prompt": system_prompt,
            "human_prompt": human_prompts,
        }
    )

    try:
        results = response.content
        return results
    except KeyError:
        raise ValueError("Failed to analyze the outline")
