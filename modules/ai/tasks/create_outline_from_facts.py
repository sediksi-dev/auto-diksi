import logging

from dotenv import load_dotenv
from helpers.md_prompt import prompt_md_by_tag
from langchain_openai import ChatOpenAI
from langchain.output_parsers import JsonOutputKeyToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel, ValidationError

from modules.ai.tools.outline_generator import OutlineArticle, outline_generator
from helpers.error_handling import error_handler

load_dotenv()


class CreateArticleFromFacts(BaseModel):
    informations: str
    lang_target: str = "indonesia"
    lang_source: str = "english"


@error_handler("ai", "Error when creating an outline from facts.")
def create_outline_from_facts(args: CreateArticleFromFacts) -> OutlineArticle:
    # Define the configuration for the OpenAI model
    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }

    # Get the system and human prompts for the analysis. The prompts are provided in markdown files and necessary variables are passed to the prompts.
    system_prompt = prompt_md_by_tag(
        "modules/ai/prompts/create_outline_from_facts.md", "SYSTEM_PROMPT"
    )
    human_prompt = prompt_md_by_tag(
        "modules/ai/prompts/create_outline_from_facts.md", "HUMAN_PROMPT"
    )

    # Initializing the model
    llm = ChatOpenAI(**openai_config)
    model = llm.bind_tools(tools=[outline_generator], tool_choice="outline_generator")
    prompts = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", human_prompt)]
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
            "informations": args.informations,
            "lang_target": args.lang_target,
            "lang_source": args.lang_source,
        },
        config={
            "run_name": "CreateOutlineFromFacts",
            "tags": ["create_outline_from_facts", "openai"],
        },
    )

    try:
        return OutlineArticle(**response["outline"])
    except ValidationError as vld_err:
        logging.error(f"Outline not created due to validation error: {str(vld_err)}")
