from langchain.pydantic_v1 import BaseModel


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
