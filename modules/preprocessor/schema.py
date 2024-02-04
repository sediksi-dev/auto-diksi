from pydantic import BaseModel


class PreprocessorConfig(BaseModel):
    content: str
    images: list[str]
    headers: list[str]
    paragraphs_count: int
