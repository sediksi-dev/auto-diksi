import os
from fastapi import FastAPI
from app.bot import routers as bot
from dotenv import load_dotenv

# from modules.supabase.db import db

load_dotenv()

auth_email = os.environ.get("SUPABASE_AUTH_EMAIL")
auth_password = os.environ.get("SUPABASE_AUTH_PASSWORD")

app = FastAPI()


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     response = await call_next(request)
#     print("From middleware", request.url.path)

#     if request.url.path.startswith("/bot"):
#         passkey = request.headers.get("X-AGC-PASSKEY")
#         if not passkey or passkey != f"{auth_email}:{auth_password}":
#             response.headers["X-AGC-PASSKEY"] = "not allowed"
#         else:
#             response.headers["X-AGC-PASSKEY"] = "allowed"

#     return response


app.include_router(bot.router)
