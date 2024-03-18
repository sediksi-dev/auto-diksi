from fastapi import APIRouter

from .crawler.controller import BotCrawler

from .writer.controller import BotRewriter

from .uploader.controller import BotUploader

from .models import CrawlerResponse, RewriterResponse, PostToWpArgs, PostToWpPayload

router = APIRouter(prefix="/bot", tags=["bot"])


@router.post(
    "/crawl",
    response_model=CrawlerResponse,
    summary="Crawl the source and save the posts to the database as draft",
)
def bot_crawler():
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
def write_drafted_post(mode: str = "default", draft_id: int = None):
    """
    This endpoint will check the 'draft' posts from database.
    """
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
def post_to_wp(data: PostToWpArgs):
    """
    This endpoint will post the drafted articles to the WordPress site.
    """
    wp = BotUploader()
    response = wp.post(data)
    return response


@router.post("/run", summary="Test the bot")
def test_bot(mode: str = "default"):
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
            featured_media=data.featured_media
        )

        wp = BotUploader()
        response = wp.post(data_to_post)

        return response

    except Exception as e:
        return {"error": str(e)}
