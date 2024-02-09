from pydantic import BaseModel, Field
from typing import Optional


class TaxonomyMapping(BaseModel):
    id: Optional[int] = Field(None, alias="id")
    source_id: int = Field(
        ..., alias="source_id", description="References an id in the taxonomies table"
    )
    target_id: int = Field(
        ..., alias="target_id", description="References an id in the taxonomies table"
    )

    class Config:
        orm_mode = True
        schema_extra = {"example": {"source_id": 1, "target_id": 2}}
