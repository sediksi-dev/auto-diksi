from fastapi import APIRouter
from .models import CrawlerResponse
from .crawler.controller import BotCrawler
from .writer.controller import BotRewriter
from typing import List

router = APIRouter(prefix="/bot", tags=["bot"])


@router.get("/test-route", summary="Test route for bot")
def test_route():
    return {"message": "Bot is working!"}


@router.post(
    "/crawl",
    response_model=List[CrawlerResponse],
    summary="Crawl the source and save the posts to the database as draft",
)
def bot_crawler():
    """
    This endpoint will check the posts from the source and save them to the database.
    It will return the list of articles that have been saved to the database.
    """
    bot = BotCrawler()
    data = bot.submit_posts()
    return data


@router.post("/rewrite")
def write_drafted_post(mode: str = "default", post_count: int = 1):
    """
    This endpoint will check the 'draft' posts from database.
    """
    bot = BotRewriter()
    data = bot.write(mode, post_count)
    return data
