from pydantic import BaseModel
from typing import Literal, Optional, Dict


class TaxMapping(BaseModel):
    source: str
    tax_id: int
    term_name: Literal["categories", "tags"]


class ArticleToTaxMapping(BaseModel):
    id: Optional[int]
    articles_id: int
    taxonomy_mapping_id: int


class ArticleMappingSource(BaseModel):
    web: Dict[str, str]


class ArticleMapping(BaseModel):
    id: Optional[int]
    source: ArticleMappingSource
    tax_id: Dict[str, int]
    terms: Dict[str, Literal["categories", "tags"]]
