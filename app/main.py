import os
from fastapi import FastAPI
from app.bot import routers as bot
from dotenv import load_dotenv

# from modules.supabase.db import db

load_dotenv()

auth_email = os.environ.get("SUPABASE_AUTH_EMAIL")
auth_password = os.environ.get("SUPABASE_AUTH_PASSWORD")

app = FastAPI()

app.include_router(bot.router)
