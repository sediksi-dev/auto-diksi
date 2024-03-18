from pydantic import BaseModel, Field
from modules.supabase.db import db
from helper.error_handling import error_handler
from .get_credentials_by_host import get_credentials_by_host, Credentials


class WebData(BaseModel):
    host: str
    path: str
    type: str


class GetWebDataByHost(BaseModel):
    web: WebData
    credentials: Credentials = Field(..., alias="auth")


@error_handler("db", "Error when getting web by host")
def get_web_by_host(host: str) -> GetWebDataByHost:
    query = (
        "host:url",
        "path:api_endpoint",
        "type:post_type",
    )
    res, _ = db.table("web").select(*query).eq("url", host).single().execute()
    result = res[1]
    web_data = {
        "host": result.get("host"),
        "path": result.get("path"),
        "type": result.get("type"),
    }

    credentials = get_credentials_by_host(host)

    return GetWebDataByHost(
        web=WebData(**web_data),
        auth=credentials,
    )
