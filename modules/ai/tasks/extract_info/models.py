from typing import List
from langchain.pydantic_v1 import BaseModel, Field


# Model for the input data for `create_outline` task
class CreateOutlineFromArticleArgs(BaseModel):
    original_article: str
    lang_target: str = "indonesia"
    lang_source: str = "english"


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
    further_insights: str = Field(
        ...,
        description="Any additional relevant information that doesn't fit directly under the created subheadings should be compiled under a 'Further Insights' section.",
    )
