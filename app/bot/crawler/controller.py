from typing import List
import requests
from modules.supabase.db import db
from helper.error_handling import error_handler

from .models import WpPostData, ArticleToTaxMapping, SubmittedArticles

from modules.supabase.query.get_web_sources import get_web_sources, WebSources
from modules.supabase.query.get_article_by_urls import get_articles_by_urls
from modules.supabase.query.insert_articles import (
    insert_articles,
    ArticleToInsert,
    Article,
)
from modules.supabase.query.get_taxonomies_map import get_taxonomies_map


class BotCrawler:
    def __init__(self, **kwargs):
        self.__multiplier = kwargs.get("multiplier", 5)
        self.__source = self.__get_sources()
        self.__unique_articles: List[WpPostData] = self.__processing_raw_articles()

    def __get_sources(self):
        sources = get_web_sources()
        return sources

    @error_handler("wp", "Error when get all wp posts from sources")
    def __get_wp_articles(self, src: WebSources) -> List[WpPostData]:
        count = len(src.taxonomies) * self.__multiplier
        per_page = count if count < 100 else 100
        query = f"?per_page={per_page}"
        url = f"https://{src.url}/{src.api_endpoint}/{src.post_type}{query}"
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            },
        )
        response.raise_for_status()
        response = response.json()
        articles = [WpPostData(**article) for article in response]
        return articles

    def __filter_posts(self, wp_posts: List[WpPostData], src: WebSources, key: str):
        source = src.model_dump()
        posts = [post.model_dump() for post in wp_posts]
        ids = [
            tax["taxonomy_id"]
            for tax in source["taxonomies"]
            if tax["term_name"] == key
        ]

        # Menyaring data post berdasarkan id
        filtered = [
            post for post in posts if key in post and any(id in post[key] for id in ids)
        ]

        return filtered

    def __processing_raw_articles(self):
        sources = self.__source
        articles: List[WpPostData] = []
        for src in sources:
            term_names = [tax.term_name for tax in src.taxonomies]
            wp_posts = self.__get_wp_articles(src)
            for term in term_names:
                filtered_posts = self.__filter_posts(wp_posts, src, term)
                articles += [WpPostData(**article) for article in filtered_posts]
        unique_articles: List[WpPostData] = []
        for article in articles:
            if article.link not in [x.link for x in unique_articles]:
                unique_articles.append(article)

        self.__unique_articles = unique_articles
        return unique_articles

    def __filtering_none_existing_articles(
        self, articles: List[WpPostData]
    ) -> List[WpPostData]:
        post_urls = [article.link for article in articles]
        chunked_urls = [post_urls[i : i + 10] for i in range(0, len(post_urls), 10)]
        posted_articles = []
        for chunk in chunked_urls:
            response = get_articles_by_urls(chunk)
            posted_articles += response
        filtered_articles = [
            article
            for article in articles
            if article.link not in [x["source_url"] for x in posted_articles]
        ]
        return filtered_articles

    def __save_articles_to_db(self, article: WpPostData) -> Article:
        prepared = ArticleToInsert(
            title=article.title.rendered,
            published_date=str(article.date),
            post_id=article.id,
            link=article.link,
        )
        inserted = insert_articles(prepared)
        return inserted

    def __get_mapping_id(self, article: WpPostData):
        return get_taxonomies_map(article)

    def __mapping_articles_to_taxonomy(
        self, post_id: int, taxonomy_mapping_id: int
    ) -> ArticleToTaxMapping:
        payload = {"articles_id": post_id, "taxonomy_mapping_id": taxonomy_mapping_id}
        response = db.table("articles_mapping").insert(payload).execute()
        return ArticleToTaxMapping(**response.data[0])

    def submit_posts(self) -> List[SubmittedArticles]:
        results = []
        wp_articles = self.__filtering_none_existing_articles(self.__unique_articles)
        for article in wp_articles:
            submitted_article = self.__save_articles_to_db(article)
            submitted_article_id = submitted_article.id
            article_obj = article.model_dump()
            tax_mapping = self.__get_mapping_id(article)
            tax_results = [
                tax
                for tax in tax_mapping
                if tax.source.tax_id in article_obj[tax.source.term]
            ]
            map_results = []
            for tax in tax_results:
                mapped = self.__mapping_articles_to_taxonomy(
                    submitted_article_id, tax.id
                )
                map_results.append(mapped)

            results.append({"article": submitted_article, "tax_mapping": map_results})
        return results
