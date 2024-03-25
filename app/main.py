from fastapi import FastAPI
from app.bot import routers as bot
from app.seeder import routers as seeder


app = FastAPI()

app.include_router(bot.router)
app.include_router(seeder.router)
