# import os
# import json
from dotenv import load_dotenv
from modules.ai.models import ArticleToArticleInput
from modules.ai.tasks.summarization import summarizer
from modules.ai.tasks.create_search_image_query import create_search_image_query

from helper.bing_image_search import BingImage

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def test_mode_rewriter(args: ArticleToArticleInput):
    article = args.original_article
    summary = summarizer(article)
    image_query = create_search_image_query(summary, is_summarized=True)
    bing = BingImage()

    results = bing.get_images(
        count=5,
        max_result=10,
        query=image_query,
    )
    if len(results) > 0:
        image_url = results[0]
        llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": f"This image represents the search query '{image_query}'. Elaborate the image with the search query to create one sentence alt text.",
                },  # You can optionally provide text parts
                {"type": "image_url", "image_url": image_url},
            ]
        )

        alt_text = llm.invoke([message])

    else:
        image_url = results
        alt_text = ''

    return {
        "original_article": args.original_article,
        "summary": summary,
        "image_query": image_query,
        "image_url": image_url,
        "alt_text": alt_text.content,
    }
