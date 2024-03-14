from langchain_core.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import List


# Model for the tools used in `create_outline` tool
class Subheading(BaseModel):
    subheading: str = Field(
        ...,
        description="The subheading for the new article based on the key information identified.",
    )
    information: List[str] = Field(
        ...,
        description="The detailed body text that expands on the identified information, maintaining relevance and coherence with the original content.",
    )


class OutlineArticle(BaseModel):
    intro: str = Field(
        ...,
        description="The introductory paragraph summarizing the article's overall theme.",
    )
    sections: List[Subheading] = Field(
        ...,
        description="Array of subheadings and detailed body text.",
    )


@tool
def outline_generator(
    outline: OutlineArticle,
) -> OutlineArticle:
    """Extracted and organized important points from the original article which is contained an article structure consisting of intro and sections."""
    return outline
