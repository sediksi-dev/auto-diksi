from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputKeyToolsParser
from langchain_core.tools import tool

from helper.md_prompt import prompt_from_md

from .models import SEOData, CreateSEODataArgs

load_dotenv()


@tool
def seo_analyst(
    seo_data: SEOData,
) -> SEOData:
    """Analyzes the outline and provides SEO data for the article. It includes the main keyword, SEO-friendly title, meta description, target audience, and writing guidelines."""
    return seo_data


def create_seo_data(args: CreateSEODataArgs) -> SEOData:
    """
    Analyzes the outline and provides SEO data for the article. It includes the main keyword, SEO-friendly title, meta description, target audience, and writing guidelines.

    Args:
        args (CreateSEODataArgs): The input data for the `create_seo_data` function.
            - outline (str): The outline of the article.
            - lang_target (str, optional): The target language for the article. Defaults to "indonesia".
    """

    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }
    system_prompt = prompt_from_md("modules/ai/tasks/create_seo_data/prompts/system.md")
    human_prompt = prompt_from_md(
        "modules/ai/tasks/create_seo_data/prompts/human.md",
        outline=args.outline,
        lang_target=args.lang_target,
    )

    llm = ChatOpenAI(**openai_config)
    model = llm.bind_tools(tools=[seo_analyst], tool_choice="seo_analyst")

    prompts = ChatPromptTemplate.from_messages(
        [("system", "{system_prompt}"), ("human", "{human_prompt}")]
    )

    analysis_seo = (
        prompts
        | model
        | JsonOutputKeyToolsParser(key_name="seo_analyst", return_single=True)
    )

    response = analysis_seo.invoke(
        {
            "system_prompt": system_prompt,
            "human_prompt": human_prompt,
        }
    )

    try:
        results = SEOData(**response["seo_data"])
        return results
    except KeyError:
        raise ValueError("Failed to analyze the outline")
