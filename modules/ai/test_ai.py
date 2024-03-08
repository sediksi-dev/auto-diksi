from .tasks.extract_info.bot import extract_info


def create_new_article(content: str):
    article = extract_info(content)
    return article
