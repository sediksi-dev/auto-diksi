from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from dotenv import load_dotenv
import os

from .crawler.controller import BotCrawler

from .writer.controller import BotRewriter

from .uploader.controller import BotUploader

from .models import CrawlerResponse, RewriterResponse, PostToWpArgs, PostToWpPayload

from helper.error_handling import AiResponseException, DatabaseException, WpException


load_dotenv()

security = HTTPBasic()
router = APIRouter(prefix="/bot", tags=["bot"])

auth_username = os.environ.get("BASIC_AUTH_USERNAME")
auth_password = os.environ.get("BASIC_AUTH_PASSWORD")


@router.post(
    "/crawl",
    response_model=CrawlerResponse,
    summary="Crawl the source and save the posts to the database as draft",
)
def bot_crawler(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)] = None,
):
    """
    This endpoint will check the posts from the source and save them to the database.
    It will return the list of articles that have been saved to the database.
    """
    if credentials.username != auth_username or credentials.password != auth_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
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
def write_drafted_post(
    mode: str = "default",
    draft_id: int = None,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)] = None,
):
    """
    This endpoint will check the 'draft' posts from database.
    """
    if credentials.username != auth_username or credentials.password != auth_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        bot = BotRewriter(draft_id)
        data = bot.write(mode)
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
def post_to_wp(
    data: PostToWpArgs,
    credentials: Annotated[HTTPBasicCredentials, Depends(security)] = None,
):
    """
    This endpoint will post the drafted articles to the WordPress site.
    """
    if credentials.username != auth_username or credentials.password != auth_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    wp = BotUploader()
    response = wp.post(data)
    return response


@router.post("/run", summary="Running the bot to rewrite, and post to WordPress")
def test_bot(
    mode: str = "default",
    credentials: Annotated[HTTPBasicCredentials, Depends(security)] = None,
):
    if credentials.username != auth_username or credentials.password != auth_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        bot = BotRewriter()
        data = bot.write(mode)

        data_to_post = PostToWpArgs(
            draft_id=data.draft_id,
            body=PostToWpPayload(
                title=data.result.title,
                content=data.result.article,
                excerpt=data.result.description,
                status="draft",
            ),
            featured_media=data.featured_media,
        )

        wp = BotUploader()
        response = wp.post(data_to_post)

        return response

    except AiResponseException as e:
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")

    except DatabaseException as e:
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")

    except WpException as e:
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Failed. Message: {str(e)}")
