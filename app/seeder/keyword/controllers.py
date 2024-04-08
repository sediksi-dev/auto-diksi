import random
import markdown as md
import datetime
from .models import FeaturedImage
from app.seeder.schemas import UploadPayload

from modules.ai.main import AI
from modules.ai.models import KeywordToArticleInput, KeywordToArticleOutput

from modules.wp.main import BasicWP, WpCredentials, WpPostData
from modules.supabase.query.get_article_seed_keywords import get_artcile_seed_data
from modules.supabase.query.get_queued_keyword import get_queued
from modules.supabase.query.check_keyword_during_date import (
    get_artcile_seed_by_date,
    update_keyword_status,
)

from helpers.bing_image_search import BingImage


class SeederKeyword:
    def __init__(self):
        pass

    def get_keyword_id(self):
        queued = get_queued()
        return queued

    def update_keyword_status(self, id: int, status: str, **kwargs):
        return update_keyword_status(id=id, status=status, **kwargs)

    def queue(self):
        results = []
        data = get_artcile_seed_by_date()
        payload = [{"id": row.id, "status": "queue"} for row in data["data"]]

        for item in payload:
            results.append(update_keyword_status(id=item["id"], status=item["status"]))
        return results

    def generate(
        self, keyword: str, lang_target: str, mode: str = "default"
    ) -> KeywordToArticleOutput:
        ai = AI()
        return ai.keyword_to_article(
            mode=mode,
            args=KeywordToArticleInput(keyword=keyword, lang_target=lang_target),
        )

    def find_featured_images(self, original_articles: str):
        ai = AI()
        bing = BingImage()
        try:
            query = ai.article_to_image_query(original_articles)
        except Exception:
            query = ai.article_to_image_query(original_articles, use_openai=True)

        images = bing.get_images(count=3, max_result=10, query=query)
        random.shuffle(images)
        if len(images) == 0:
            raise ValueError("No images found")

        image_url = images[0]
        try:
            alt_text = ai.generate_alt_text(image_url, query)
        except Exception:
            alt_text = "A picture of a " + query

        return FeaturedImage(
            url=image_url,
            alt=alt_text,
            title=f"A picture of a {query}",
            caption=alt_text,
        )

    def upload(self, draft_id: int, args: UploadPayload):
        wp = BasicWP()
        seed = get_artcile_seed_data(draft_id)

        target_url = (
            f"https://{seed.web.url}/{seed.web.api_endpoint}/{seed.web.post_type}"
        )
        target_media_url = f"https://{seed.web.url}/{seed.web.api_endpoint}/media"

        image_id = wp.image_upload(
            target_url=target_media_url,
            image_url=args.image.url,
            credentials=WpCredentials(
                username=seed.credentials.username,
                token=seed.credentials.password,
            ),
            title=args.image.title,
            caption=args.image.caption,
            alt_text=args.image.alt,
            return_id=True,
        )

        utctime = datetime.datetime.strptime(seed.publish_date, "%Y-%m-%dT%H:%M:%S")
        timezone = datetime.timezone(datetime.timedelta(hours=7))
        localtime = utctime.astimezone(timezone)

        post_data = WpPostData(
            title=args.article.title,
            excerpt=args.article.description,
            content=md.markdown(args.article.article),
            status=seed.publish_status,
            date=localtime,
            taxonomies={seed.tax.term: str(seed.tax.tax_id)},
        )
        if image_id is not None:
            post_data.featured_media = image_id

        try:
            response = wp.post_to_wp(
                url=target_url,
                credentials=WpCredentials(
                    username=seed.credentials.username,
                    token=seed.credentials.password,
                ),
                payload=post_data,
            )
            return response
        except Exception as e:
            raise ValueError(f"Error uploading to WordPress: {e}")
