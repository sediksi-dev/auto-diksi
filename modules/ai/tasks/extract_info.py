from dotenv import load_dotenv

from helpers.md_prompt import prompt_md_by_tag

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_openai import ChatOpenAI


from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_core.prompts import ChatPromptTemplate
from helpers.error_handling import error_handler

load_dotenv()


@error_handler("ai", "Error when extracting information from the article.")
def extract_info(original_article: str):
    template_prompts = prompt_md_by_tag(
        "modules/ai/prompts/extract_info.md",
        "TEMPLATE_PROMPT",
    )

    facts_prompt = ChatPromptTemplate.from_template(template_prompts)

    llm_google = ChatGoogleGenerativeAI(model="gemini-1.0-pro")

    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }
    llm_openai = ChatOpenAI(**openai_config)

    google_chain = (
        {"original_article": RunnablePassthrough()}
        | facts_prompt
        | llm_google
        | StrOutputParser()
    )
    openai_chain = (
        {"original_article": RunnablePassthrough()}
        | facts_prompt
        | llm_openai
        | StrOutputParser()
    )

    try:
        google_output = google_chain.invoke(
            {"original_article": original_article},
            config={
                "run_name": "ExractInformations",
                "tags": ["extract_info", "google"],
            },
        )
        return google_output
    except Exception as e:
        print("Google failed, trying OpenAI", "Error:", e)
        openai_output = openai_chain.invoke(
            {"original_article": original_article},
            config={
                "run_name": "ExractInformations",
                "tags": ["extract_info", "openai"],
            },
        )
        return openai_output
