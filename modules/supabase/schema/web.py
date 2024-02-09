from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum


class WebRole(str, Enum):
    source = "source"
    target = "target"


class Web(BaseModel):
    id: Optional[int] = Field(None, alias="id")
    url: str = Field(..., alias="url")
    api_endpoint: str = Field("wp-json/wp/v2/posts", alias="api_endpoint")
    auth_username: Optional[str] = Field(None, alias="auth_username")
    auth_token: Optional[str] = Field(None, alias="auth_token")
    role_key: WebRole = Field(..., alias="role_key")

    class Config:
        orm_mode = True

    @validator("auth_username", "auth_token", always=True)
    def check_auth_details(cls, v, values, field):
        if "role_key" in values and values["role_key"] == WebRole.target:
            if not v:
                raise ValueError(
                    f'{field.name} tidak boleh kosong ketika role_key adalah "target"'
                )
        return v
