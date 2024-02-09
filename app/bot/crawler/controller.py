from modules.supabase.db import db
from modules.supabase.schema.articles import Article
from .models.sources import SourceModel, SourceTaxonomies
from .models.articles import RawArticles, ProcessedArticles, PreparedArticles
from .models.mapping import TaxMapping, ArticleToTaxMapping, ArticleMapping
from typing import List
import requests


class BotCrawler:
    def __init__(self):
        self.__query = (
            "id",
            "url",
            "api_endpoint",
            "post_type",
            "taxonomies(term_name, taxonomy_id, taxonomy_name)",
        )
        self.source = self.__get_sources()

    def __get_sources(self) -> List[SourceModel]:
        query = self.__query
        response = db.table("web").select(*query).eq("role_key", "source").execute()
        results = [SourceModel(**x) for x in response.data]
        return results

    def __get_articles_from_sources(
        self, src: SourceModel, tax: SourceTaxonomies, per_page: int = 5
    ) -> List[RawArticles]:
        query = f"?{tax.term_name}={tax.taxonomy_id}&per_page={per_page}"
        url = f"https://{src.url}/{src.api_endpoint}/{src.post_type}{query}"
        response = requests.get(url).json()
        articles = [RawArticles(**article) for article in response]
        return articles

    def __processing_raw_articles(self) -> List[ProcessedArticles]:
        sources = self.source
        articles = []
        for src in sources:
            for tax in src.taxonomies:
                items = self.__get_articles_from_sources(src, tax)
                data = ProcessedArticles(source=src, taxonomies=tax, articles=items)
                articles.append(data)
        return articles

    def __formating_articles(self, obj: ProcessedArticles) -> List[PreparedArticles]:
        result: List[PreparedArticles] = []
        for article in obj.articles:
            item = PreparedArticles(
                published_date=article.date,
                title=article.title.rendered,
                link=article.link,
                post_id=article.id,
                source=obj.source.url,
                taxonomies=[obj.taxonomies],
            )
            result.append(item)
        return result

    def __get_all_articles(self) -> List[PreparedArticles]:
        articles = self.__processing_raw_articles()

        result = []
        for article in articles:
            items = self.__formating_articles(article)
            result.extend(items)

        unique_result = []
        for item in result:
            exist = next(
                (
                    x
                    for x in unique_result
                    if x.source == item.source and x.post_id == item.post_id
                ),
                None,
            )
            if exist:
                exist.taxonomies.extend(item.taxonomies)
            else:
                unique_result.append(item)

        return unique_result

    def __filtering_none_existing_articles(
        self, articles: List[PreparedArticles]
    ) -> List[PreparedArticles]:
        post_urls = [article.link for article in articles]
        response = (
            db.table("articles")
            .select("source_url")
            .in_("source_url", post_urls)
            .execute()
        )
        posted_articles = response.data
        filtered_articles = [
            article
            for article in articles
            if article.link not in [x["source_url"] for x in posted_articles]
        ]
        return filtered_articles

    def __save_articles_to_db(self, article: PreparedArticles) -> Article:
        response = (
            db.table("articles")
            .insert(
                {
                    "post_title": article.title,
                    "published_date": str(article.published_date),
                    "original_id": article.post_id,
                    "source_url": article.link,
                }
            )
            .execute()
        )
        results = response.data[0]
        return Article(**results)

    def __get_mapping_id(self, data: TaxMapping) -> int:
        query = (
            "id",
            "terms:source_id!inner(term_name)",
            "tax_id:source_id!inner(taxonomy_id)",
            "source:source_id!inner(web(url))",
        )
        filter_query = {
            "terms.term_name": data.term_name,
            "tax_id.taxonomy_id": data.tax_id,
            "source.web.url": data.source,
        }
        res = db.table("taxonomy_mapping").select(*query).match(filter_query).execute()
        res_data = res.data[0]
        mapping = ArticleMapping(**res_data)
        return mapping.id

    def __mapping_articles_to_taxonomy(self, post_id: int, taxonomy_mapping_id: int) -> ArticleToTaxMapping:
        payload = {"articles_id": post_id, "taxonomy_mapping_id": taxonomy_mapping_id}
        response = db.table("articles_mapping").insert(payload).execute()
        return ArticleToTaxMapping(**response.data[0])

    def submit_posts(self) :
        result = []
        articles = self.__get_all_articles()
        filtered_articles = self.__filtering_none_existing_articles(articles)

        for article in filtered_articles:
            response = self.__save_articles_to_db(article)
            post_id = response.id
            tax = []
            for taxonomy in article.taxonomies:
                mapping_id = self.__get_mapping_id(
                    TaxMapping(
                        source=article.source,
                        tax_id=taxonomy.taxonomy_id,
                        term_name=taxonomy.term_name,
                    )
                )
                res = self.__mapping_articles_to_taxonomy(post_id, mapping_id)
                tax.append(res)
            result.append({"article": response, "taxonomies": tax})
        return result
