from dotenv import load_dotenv
from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.pydantic_v1 import BaseModel
from langchain_core.output_parsers import StrOutputParser
from helper.error_handling import error_handler
from helper.md_prompt import prompt_md_by_tag

load_dotenv()


class CreateSectionParagraphArgs(BaseModel):
    outline: str
    intro: str
    lang_target: str = "indonesia"

    keyword: str
    title: str
    target_audience: str = "specific target audience"
    intent: str = "informative"
    style: str = "formal"
    tone: str = "neutral"

    section_title: str
    informations: List[str]


@error_handler("ai", "Error when creating a section paragraphs.")
def create_section_paragraphs(args: CreateSectionParagraphArgs) -> str:
    """ """
    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }
    system_prompt = prompt_md_by_tag(
        "modules/ai/prompts/create_section_paragraphs.md", "SYSTEM_PROMPT"
    )

    human_prompt = prompt_md_by_tag(
        "modules/ai/prompts/create_section_paragraphs.md", "HUMAN_PROMPT"
    )

    # Initializing the model
    model = ChatOpenAI(**openai_config)

    prompts = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", human_prompt)]
    )

    # Defining the pipeline for analyzing the outline
    analysis_seo = prompts | model | StrOutputParser()

    response = analysis_seo.invoke(
        {
            "outline": args.outline,
            "intro": args.intro,
            "lang_target": args.lang_target,
            "keyword": args.keyword,
            "title": args.title,
            "target_audience": args.target_audience,
            "intent": args.intent,
            "style": args.style,
            "tone": args.tone,
            "section_title": args.section_title,
            "informations": "\n".join([f"• {info}" for info in args.informations]),
        },
        config={
            "run_name": "CreateSectionParagraphs",
            "tags": ["create_section_paragraphs", "openai"],
        },
    )

    try:
        results = response
        return results
    except KeyError:
        raise ValueError("Failed to analyze the outline")
