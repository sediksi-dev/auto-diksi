from pydantic import BaseModel
from typing import Literal
from modules.ai.models import KeywordToArticleOutput


# Schema for any response that will be sent by the API
class DefaultResponse(BaseModel):
    status: Literal["success", "error"]
    message: str = ""


class GenerateResponse(DefaultResponse):
    data: KeywordToArticleOutput
