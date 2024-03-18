from dotenv import load_dotenv
import re
from helper.md_prompt import prompt_md_by_tag

# from langchain.pydantic_v1 import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnableLambda
from helper.error_handling import error_handler

load_dotenv()


def get_image_query(text: str) -> str:
    """Get an image query from the response of the AI model."""
    # Example Input: [IMAGE QUERY]The Eiffel Tower at night[/IMAGE QUERY]
    # Example Output: The Eiffel Tower at night

    text = text.strip()

    # Remove the [IMAGE QUERY] and [/IMAGE QUERY] tags
    text = re.sub(r"\[IMAGE QUERY\]", "", text)
    text = re.sub(r"\[/IMAGE QUERY\]", "", text)

    # Remove any leading or trailing whitespace
    query = text.strip()

    # Remove any symbols that are not letters, numbers, or spaces
    query = re.sub(r"[^\w\s]", "", query)

    # Remove any quotes from the query
    query = query.replace('"', "")
    query = query.replace("'", "")

    return query


@error_handler("ai", "Error when creating a search image query.")
def create_search_image_query(text: str, is_summarized=False) -> str:
    """Create a query from article to search for an image."""

    if not is_summarized:
        prompt_tag = "FROM_ARTICLE"
    else:
        prompt_tag = "FROM_SUMMARY"

    prompt = prompt_md_by_tag(
        "modules/ai/prompts/create_search_image_query.md",
        prompt_tag,
    )
    prompt = ChatPromptTemplate.from_template(prompt)

    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro")

    chain = prompt | llm | StrOutputParser() | RunnableLambda(get_image_query)

    query = chain.invoke(
        {"text": text},
        config={
            "run_name": "CreateSearchImageQuery",
            "tags": ["create_search_image_query"],
        },
    )

    return query
