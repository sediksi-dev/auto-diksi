from typing import Literal
from langchain_core.pydantic_v1 import BaseModel, Field


# Define the models for input data used by `create_seo_data` function
class CreateSEODataArgs(BaseModel):
    outline: str
    lang_target: str = "indonesia"


# Define the models for the tool used by `create_seo_data` function
class WritingGuidelines(BaseModel):
    intent: Literal["informative", "educational", "inspirational", "entertaining"] = (
        Field(
            ...,
            description="Intent of the article. It describes the purpose of the article and what the writer wants to achieve with it.",
        )
    )
    style: str = Field(
        ...,
        description="Style of the article. It describes the way the article is written and the language used.",
    )
    tone: str = Field(
        ...,
        description="Tone of the article. It describes the attitude of the writer towards the subject and the readers.",
    )


class SEOData(BaseModel):
    keyword: str = Field(
        ...,
        description="Main keyword for the article. It should be specific and consist of at least 3 words.",
    )
    seo_title: str = Field(
        ...,
        description="SEO-friendly title for the article. It should be engaging and contain the main keyword.",
    )
    meta_description: str = Field(
        ...,
        description="SEO-friendly meta description for the article. It should be concise and contain the main keyword.",
    )
    target_audience: str = Field(
        ...,
        description="Target audience for the article. It describes the group of people the article is intended for.",
    )
    writing_guidelines: WritingGuidelines = Field(
        ...,
        description="Writing guidelines for the article. It describes the intent, style, and tone of the article.",
    )
