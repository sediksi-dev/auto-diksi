from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
)

from helpers.auth import auth
from modules.supabase.query.update_article import update_article

from .crawl.controller import BotCrawler

from .rewrite.controller import BotRewriter

from .uploader.controller import BotUploader

from .drafter.controllers import BotDrafter

from .schemas import (
    CrawlerResponse,
    DrafterResponse,
    RewriterResponse,
    UploaderPayload,
    UploaderResponse,
)


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
        if len(data) == 0:
            return {
                "status": "success",
                "message": "No new articles found in the sources.",
                "data": data,
            }

        return {
            "status": "success",
            "message": f"{len(data)} articles have been saved to the database.",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to crawling new post in sources. Message: {str(e)}",
        )


@router.post(
    "/draft",
    description="Get the drafted posts from each source in the database",
    response_model=DrafterResponse,
)
async def get_draft_posts():
    """
    This endpoint will check the 'draft' posts from database.
    """
    bot = BotDrafter()
    try:
        data = bot.get_articles_by_source_id()
        if len(data) == 0:
            return {
                "status": "success",
                "message": "No draft articles found in the database.",
                "data": data,
            }

        return {
            "status": "success",
            "message": f"{len(data)} draft articles found in the database.",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to get draft posts from database. Message: {str(e)}",
        )


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
        data = bot.rewrite()
        return {
            "status": "success",
            "message": "The articles have been rewritten.",
            "data": data,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")


@router.post(
    "/upload",
    summary="Post the rewrited articles to the WordPress site",
    response_model=UploaderResponse,
)
async def post_to_wp(
    data: UploaderPayload,
):
    """
    This endpoint will post the drafted articles to the WordPress site.
    """

    wp = BotUploader()
    try:
        response = wp.post(data)
        return {
            "status": "success",
            "message": "The articles have been posted to the WordPress site.",
            "data": response,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")


@router.post("/run", summary="Running the bot to rewrite, and post to WordPress")
async def running_bot():
    try:
        bot = BotRewriter()
        draft_id = bot.db_data.draft_id
        update_article(draft_id, data={"status": "pending"})

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

            update_article(
                draft_id,
                data={
                    "status": "pending",
                    "post_id": response.id,
                    "public_url": (
                        response.link if response.link else response.guid.rendered
                    ),
                },
            )

            return response

        except Exception as e:
            update_article(draft_id, data={"status": "error"})
            raise ValueError("Validation gagal. {}".format(str(e)))

    except Exception as e:
        update_article
        raise HTTPException(status_code=400, detail=f"Failed. Message: {str(e)}")
