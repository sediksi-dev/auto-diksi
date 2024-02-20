from langchain.pydantic_v1 import BaseModel
from typing import List


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

    subtopic: str
    informations: List[str]
