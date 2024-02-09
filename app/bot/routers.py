from fastapi import APIRouter
from .models import CrawlerResponse
from .crawler.controller import BotCrawler
from .writer.controller import BotWriter
from typing import List

router = APIRouter(prefix="/bot", tags=["bot"])


@router.get("/")
def read_root():
    bot = BotCrawler()
    config = bot.source
    return config


@router.post("/crawl", response_model=List[CrawlerResponse])
def scrapper():
    """
    This endpoint will check the posts from the source and save them to the database.
    It will return the list of articles that have been saved to the database.
    """
    bot = BotCrawler()
    data = bot.submit_posts()
    return data


@router.post("/write")
def write_drafted_post(post_count: int = 1):
    """
    This endpoint will check the 'draft' posts from database.
    """
    bot = BotWriter()
    data = bot.write(post_count)
    return data
