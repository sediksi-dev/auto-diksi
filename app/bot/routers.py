import os
from dotenv import load_dotenv

from fastapi import (
    APIRouter,
    HTTPException,
    # Depends,
    Security,
    Response,
)
from fastapi.security import APIKeyHeader
from .crawler.controller import BotCrawler

from .writer.controller import BotRewriter

from .uploader.controller import BotUploader

from .models import CrawlerResponse, RewriterResponse, PostToWpArgs

from helper.error_handling import AiResponseException, DatabaseException, WpException

load_dotenv()

auth_email = os.environ.get("API_KEY_EMAIL")
auth_password = os.environ.get("API_KEY_PASSWORD")


async def auth(
    response: Response,
    passkey=Security(APIKeyHeader(name="X-AGC-PASSKEY")),
):
    split_passkey = passkey.split(":")
    email = split_passkey[0]
    password = split_passkey[1]
    if email != auth_email or password != auth_password:
        response.headers["X-AGC-PASSKEY"] = "not allowed"
        raise HTTPException(status_code=403, detail="Invalid API Key")
    response.headers["X-AGC-PASSKEY"] = "allowed"
    return True


router = APIRouter(
    prefix="/bot",
    tags=["bot"],
    # dependencies=[Depends(auth)],
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
async def write_drafted_post(
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
    data: PostToWpArgs,
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
        status = bot.db_data.model_dump()["target"][0]["config"]["post_status"]
        draft_id = bot.db_data.draft_id

        data = bot.rewrite()

        payload = {
            "draft_id": draft_id,
            "body": {
                "title": data.result.title,
                "content": data.result.article,
                "excerpt": data.result.description,
                "status": status,
            },
            "featured_media": data.featured_media,
        }

        try:
            data_to_post = PostToWpArgs.model_validate(payload)
            wp = BotUploader()
            response = wp.post(data_to_post)
            return response

        except Exception as e:
            raise ValueError("Validation gagal. {}".format(str(e)))

    except AiResponseException as e:
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")

    except DatabaseException as e:
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")

    except WpException as e:
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Failed. Message: {str(e)}")


@router.get("/test")
def test_bot(id: int):
    bt = BotRewriter(id)
    return bt.rewrite()
