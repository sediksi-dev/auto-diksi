import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security, Response
from fastapi.security import APIKeyHeader


load_dotenv()
auth_email = os.environ.get("API_KEY_EMAIL")
auth_password = os.environ.get("API_KEY_PASSWORD")


async def auth(
    response: Response,
    passkey=Security(APIKeyHeader(name="X-AGC-PASSKEY")),
):
    split_passkey = passkey.split(":")
    email = split_passkey[0]
    password = split_passkey[1]
    if email != auth_email or password != auth_password:
        response.headers["X-AGC-PASSKEY"] = "not allowed"
        raise HTTPException(status_code=403, detail="Invalid API Key")
    response.headers["X-AGC-PASSKEY"] = "allowed"
    return True
