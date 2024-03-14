from langchain_core.tools import tool
from langchain_core.pydantic_v1 import BaseModel, Field


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
        description="The group of people the article is intended for. It should be specific and well-defined",
    )
    intent: str = Field(
        ...,
        description="The main purpose of the article. It describes the reason for writing the article.",
    )
    style: str = Field(
        ...,
        description="The way the article is written. It must be consistent and appropriate for the target audience.",
    )
    tone: str = Field(
        ...,
        description="Attitude or emotionality of the article. It should be consistent and appropriate for the target audience.",
    )


@tool
def seo_analyst(
    seo_data: SEOData,
) -> SEOData:
    """SEO data for the article as a result of a very depth analysis from the outline"""
    return seo_data
