from pydantic import BaseModel


class DraftedArticles(BaseModel):
    id: int
    source: str
    title: str
    status: str
    date: str
