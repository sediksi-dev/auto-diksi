from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from helpers.error_handling import error_handler

load_dotenv()


@error_handler("ai", "Cannot add image to text.")
def create_alt_text(image_url: str, image_query: str):
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
    return alt_text.content
