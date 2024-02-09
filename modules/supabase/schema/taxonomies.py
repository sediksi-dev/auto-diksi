from pydantic import BaseModel, Field
from typing import Optional


class Taxonomy(BaseModel):
    id: Optional[int] = Field(None, alias="id")
    term_name: str = Field(..., alias="term_name")
    taxonomy_id: int = Field(..., alias="taxonomy_id")
    taxonomy_name: str = Field(..., alias="taxonomy_name")
    web_id: int = Field(..., alias="web_id")

    class Config:
        orm_mode = True
