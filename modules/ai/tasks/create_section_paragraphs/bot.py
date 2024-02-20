from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from helper.md_prompt import prompt_from_md

from .models import CreateSectionParagraphArgs

load_dotenv()


def create_section_paragraphs(args: CreateSectionParagraphArgs) -> str:
    """ """
    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }
    system_prompt = prompt_from_md(
        "modules/ai/tasks/create_section_paragraphs/prompts/system.md",
        style=args.style,
        tone=args.tone,
        intent=args.intent,
        target_audience=args.target_audience,
        outline=args.outline,
        intro=args.intro,
    )

    human_prompts = prompt_from_md(
        "modules/ai/tasks/create_section_paragraphs/prompts/human.md",
        title=args.title,
        keyword=args.keyword,
        subtopic=args.subtopic,
        informations="\n".join([f"- {info}" for info in args.informations]),
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
