from pydantic import BaseModel, Field
from modules.supabase.db import db


class Credentials(BaseModel):
    user: str
    pass_: str = Field(..., alias="pass")


class WebData(BaseModel):
    host: str
    path: str
    type: str


class GetWebDataByHost(BaseModel):
    web: WebData
    credentials: Credentials = Field(..., alias="auth")


def get_web_by_host(host: str) -> GetWebDataByHost:
    query = (
        "host:url",
        "path:api_endpoint",
        "type:post_type",
        "user: auth_username",
        "pass: auth_token",
    )
    res, _ = db.table("web").select(*query).eq("url", host).single().execute()
    result = res[1]
    web_data = {
        "host": result.get("host"),
        "path": result.get("path"),
        "type": result.get("type"),
    }
    credentials = {"user": result.get("user"), "pass": result.get("pass")}

    return GetWebDataByHost(
        web=WebData(**web_data),
        auth=Credentials(**credentials),
    )
