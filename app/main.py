from fastapi import FastAPI
from app.bot import routers as bot


app = FastAPI()
app.include_router(bot.router)
