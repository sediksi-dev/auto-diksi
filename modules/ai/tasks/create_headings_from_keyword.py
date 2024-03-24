from dotenv import load_dotenv

from helpers.md_prompt import prompt_md_by_tag

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_openai import ChatOpenAI

from langchain.output_parsers import ResponseSchema, StructuredOutputParser


from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_core.prompts import ChatPromptTemplate
from helpers.error_handling import error_handler

load_dotenv()

response_schemas = [
    ResponseSchema(
        name="sections",
        type="list of objects with keys 'subheading' and 'informations'",
        description="List of sections with headings and explanations.",
    ),
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()


@error_handler("ai", "Error when create headings from keyword.")
def create_headings_from_keyword(keyword: str, lang_target: str):

    chain = (
        {
            "keyword": RunnablePassthrough(),
            "lang_target": RunnablePassthrough(),
        }
        | outline_chain()
        | {
            "text": RunnablePassthrough(),
            "keyword": RunnablePassthrough(),
            "lang_target": RunnablePassthrough(),
            "format_instructions": RunnablePassthrough(),
        }
        | jsonify()
    )
    output = chain.invoke(
        {
            "keyword": keyword,
            "lang_target": lang_target,
            "text": RunnablePassthrough(),
            "format_instructions": format_instructions,
        },
        config={
            "run_name": "CreateHeadingsFromKeyword",
            "tags": ["create_headings_from_keyword"],
        },
    )

    return output


def outline_chain():
    llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro")
    template_prompts = prompt_md_by_tag(
        "modules/ai/prompts/create_headings_from_keyword.md",
        "TEMPLATE_PROMPT",
    )
    prompt = ChatPromptTemplate.from_template(template_prompts)
    chain = prompt | llm | StrOutputParser()
    return chain


def jsonify():
    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }
    llm = ChatOpenAI(**openai_config)
    prompt = ChatPromptTemplate.from_template(
        """Please generate json structured title, headings and explanations for keyword {keyword} in language {lang_target} from the provided outline text.
Provided text: {text}.
Format instructions: {format_instructions}.""",
    )

    chain = prompt | llm | output_parser
    return chain
