from pydantic import BaseModel, Field
from helper.error_handling import error_handler
from .get_web_config import get_web_config


class Credentials(BaseModel):
    user: str
    pass_: str = Field(..., alias="pass")


@error_handler("db", "Error when getting credentials")
def get_credentials_by_host(host: str) -> Credentials:
    config = get_web_config(host)
    auth_username = config["auth_username"]
    auth_token = config["auth_token"]
    credentials = {
        "user": auth_username,
        "pass": auth_token,
    }

    return Credentials(**credentials)
