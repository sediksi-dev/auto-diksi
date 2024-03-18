from langchain.pydantic_v1 import BaseModel
from helper.md_prompt import prompt_md_by_tag
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from helper.error_handling import error_handler


# Define the models for input data used by `create_intro` function
class CreateIntroArgs(BaseModel):
    keyword: str
    title: str
    description: str
    lang_target: str = "indonesia"
    intro_guideline: str = ""
    intent: str = "informative"
    style: str = "formal"
    tone: str = "neutral"


@error_handler("ai", "Error when creating an intro")
def create_intro(args: CreateIntroArgs) -> str:
    # Define the configuration for the OpenAI model
    openai_config = {
        "model": "gpt-3.5-turbo-0125",
        "temperature": 1,
        "max_tokens": 4000,
    }

    system_prompt = prompt_md_by_tag(
        "modules/ai/prompts/create_intro.md", "SYSTEM_PROMPT"
    )

    human_prompt = prompt_md_by_tag(
        "modules/ai/prompts/create_intro.md", "HUMAN_PROMPT"
    )

    # Initializing the model
    model = ChatOpenAI(**openai_config)

    prompts = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", human_prompt)]
    )

    create_intro = prompts | model

    response = create_intro.invoke(
        {
            "keyword": args.keyword,
            "title": args.title,
            "description": args.description,
            "lang_target": args.lang_target,
            "intro_guideline": args.intro_guideline,
            "intent": args.intent,
            "style": args.style,
            "tone": args.tone,
        },
        config={"run_name": "CreateIntro", "tags": ["create_info", "openai"]},
    )

    results = response.content
    return results
