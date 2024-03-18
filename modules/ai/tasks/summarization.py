from dotenv import load_dotenv
from helper.md_prompt import prompt_md_by_tag

# from langchain.pydantic_v1 import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from helper.error_handling import error_handler
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


@error_handler("ai", "Error when summarizing an article.")
def summarizer(article: str) -> str:
    """Summarize an article."""
    prompt = prompt_md_by_tag(
        "modules/ai/prompts/summarization.md",
        "TEMPLATE_PROMPT",
    )
    prompt = ChatPromptTemplate.from_template(prompt)

    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro")

    chain = prompt | llm | StrOutputParser()

    summary = chain.invoke(
        {"article": article},
        config={
            "run_name": "Summarization",
            "tags": ["summarization"],
        },
    )

    return summary
