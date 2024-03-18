from pydantic import BaseModel, Field
from modules.supabase.db import db


class GetCredentialsByHost(BaseModel):
    user: str
    pass_: str = Field(..., alias="pass")


def get_credentials_by_host(host: str) -> GetCredentialsByHost:
    query = (
        "user: auth_username",
        "pass: auth_token",
    )
    res, _ = db.table("web").select(*query).eq("url", host).single().execute()
    result = res[1]
    return GetCredentialsByHost(**result)
