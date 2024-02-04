from fastapi import FastAPI
from app.scrapper import routers as scrapper
from app.submitter import routers as submitter


app = FastAPI()
app.include_router(scrapper.router)
app.include_router(submitter.router)
