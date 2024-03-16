from typing import List
from fastapi import APIRouter

from .crawler.models.articles import SubmittedArticles
from .crawler.controller import BotCrawler

from .writer.controller import BotRewriter

from .models import PostToWpArgs

from modules.wp.main import WP

# from modules.wp.models import WpPostData

router = APIRouter(prefix="/bot", tags=["bot"])


@router.post(
    "/crawl",
    response_model=List[SubmittedArticles],
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


@router.post("/rewrite", summary="Rewrite the drafted posts")
def write_drafted_post(mode: str = "default", id: int = None):
    """
    This endpoint will check the 'draft' posts from database.
    """
    bot = BotRewriter(id)
    data = bot.write(mode)
    return data


@router.post("/wp", summary="Post the drafted articles to the WordPress site")
def post_to_wp(draft_id: int, data: PostToWpArgs):
    """
    This endpoint will post the drafted articles to the WordPress site.
    """
    wp = WP()
    response = wp.post_to_wp(draft_id, data=data)
    return response
