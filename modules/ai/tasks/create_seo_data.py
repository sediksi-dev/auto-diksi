from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import JsonOutputKeyToolsParser
from langchain.pydantic_v1 import BaseModel

from helper.md_prompt import prompt_md_by_tag
from helper.error_handling import error_handler
from modules.ai.tools.seo_analyst import SEOData, seo_analyst

load_dotenv()


# Define the models for input data used by `create_seo_data` function
class CreateSEODataArgs(BaseModel):
    outline: str
    lang_target: str = "indonesia"


@error_handler("ai", "Error when creating SEO data")
def create_seo_data(args: CreateSEODataArgs) -> SEOData:
    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }
    system_prompt = prompt_md_by_tag(
        "modules/ai/prompts/create_seo_data.md", "SYSTEM_PROMPT"
    )
    human_prompt = prompt_md_by_tag(
        "modules/ai/prompts/create_seo_data.md", "HUMAN_PROMPT"
    )

    llm = ChatOpenAI(**openai_config)
    model = llm.bind_tools(tools=[seo_analyst], tool_choice="seo_analyst")

    prompts = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", human_prompt)]
    )

    analysis_seo = (
        prompts
        | model
        | JsonOutputKeyToolsParser(key_name="seo_analyst", return_single=True)
    )

    response = analysis_seo.invoke(
        {
            "outline": args.outline,
            "lang_target": args.lang_target,
        },
        config={
            "run_name": "CreateSeoData",
            "tags": ["create_seo_data", "openai"],
        },
    )

    try:
        results = SEOData(**response["seo_data"])
        return results
    except KeyError:
        raise ValueError("Failed to analyze the outline")
