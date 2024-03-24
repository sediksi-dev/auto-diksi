import os
from dotenv import load_dotenv

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
)

from helpers.auth import auth

from .crawl.controller import BotCrawler

from .rewrite.controller import BotRewriter

from .uploader.controller import BotUploader

from .schemas import CrawlerResponse, RewriterResponse, UploaderPayload

load_dotenv()

auth_email = os.environ.get("API_KEY_EMAIL")
auth_password = os.environ.get("API_KEY_PASSWORD")


router = APIRouter(
    prefix="/bot",
    tags=["bot"],
    dependencies=[Depends(auth)],
)


@router.post(
    "/crawl",
    response_model=CrawlerResponse,
    summary="Crawl the source and save the posts to the database as draft",
)
async def bot_crawler():
    """
    This endpoint will check the posts from the source and save them to the database.
    It will return the list of articles that have been saved to the database.
    """
    bot = BotCrawler()
    try:
        data = bot.submit_posts()
        return {
            "status": "success",
            "message": f"{len(data)} articles have been saved to the database.",
            "data": data,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": [],
        }


@router.post(
    "/rewrite", response_model=RewriterResponse, summary="Rewrite the drafted posts"
)
async def rewriting_drafted_articles(
    draft_id: int = None,
):
    """
    This endpoint will check the 'draft' posts from database.
    """
    try:
        bot = BotRewriter(draft_id)
        data = bot.write()
        return {
            "status": "success",
            "message": "The articles have been rewritten.",
            "data": data,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": None,
        }


@router.post("/uploader", summary="Post the rewrited articles to the WordPress site")
async def post_to_wp(
    data: UploaderPayload,
):
    """
    This endpoint will post the drafted articles to the WordPress site.
    """
    wp = BotUploader()
    response = wp.post(data)
    return response


@router.post("/run", summary="Running the bot to rewrite, and post to WordPress")
def running_bot():
    try:
        bot = BotRewriter()
        draft_id = bot.db_data.draft_id

        data = bot.rewrite()

        try:
            data_to_post = UploaderPayload.model_validate(
                {
                    "draft_id": draft_id,
                    "body": {
                        "title": data.result.title,
                        "content": data.result.article,
                        "excerpt": data.result.description,
                    },
                    "featured_media": data.featured_media,
                }
            )
            wp = BotUploader()
            response = wp.post(data_to_post)
            return response

        except Exception as e:
            raise ValueError("Validation gagal. {}".format(str(e)))

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")
