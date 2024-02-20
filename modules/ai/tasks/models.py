from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class TopicsAndFacts(BaseModel):
    topics: str = Field(
        ...,
        description="The identified topic within the original article",
    )
    facts: List[str] = Field(
        ...,
        description="Associated facts with the identified topic within the original article. Must have more than two facts",
    )


class SeoData(BaseModel):
    seo_title: str = Field(
        ...,
        description="The SEO title for the input article.",
    )
    seo_description: str = Field(
        ...,
        description="The SEO description for the input article.",
        max_length=160,
    )
    main_keyword: str = Field(
        ...,
        description="The main keyword for the input article. The keyword must be present the whole article.",
    )
    additional_keywords: List[str] = Field(
        ...,
        description="Additional keywords for the input article. At least 3 additional keywords must be present in the article.",
    )


class Summary(BaseModel):
    summary: str = Field(
        ...,
        description="The summary of the input article.",
        max_length=500,
    )
