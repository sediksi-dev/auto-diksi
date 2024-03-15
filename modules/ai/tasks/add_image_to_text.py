import random
from dotenv import load_dotenv

from modules.ai.tasks.create_search_image_query import create_search_image_query
from helper.bing_image_search import BingImage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()


def add_image_to_text(text: str):
    image_query = create_search_image_query(text, is_summarized=True)
    bing = BingImage()
    images = bing.get_images(
        count=3,
        max_result=10,
        query=image_query,
    )
    if len(images) > 0:
        random.shuffle(images)
        image_url = images[0]
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
        md_image = f"![{alt_text.content}]({image_url} '{image_query}')"
        return md_image + "\n" + text
    else:
        return text
