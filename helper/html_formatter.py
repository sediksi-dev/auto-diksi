from app.bot.writer.models.articles import ArticleWriteOutput
from bs4 import BeautifulSoup
import markdown


def format_data_to_html(data: ArticleWriteOutput) -> str:
    intro = data.content.rewrited.intro
    body = data.content.rewrited.body
    images = data.images.body_images
    iframe = data.iframe.link

    intro_html = markdown.markdown(intro)
    body_html = "\n".join([markdown.markdown(b) for b in body])
    article = f"{intro_html}\n{body_html}"
    images_html = [f'<img src="{i}" />' for i in images]
    iframe_html = [f'<iframe src="{i}" />' for i in iframe]

    # parse article to html using bs4
    soup = BeautifulSoup(article, "html.parser")

    # match count of images and iframes to the count of headings
    # and insert them after each heading
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    for i, img in enumerate(images_html):
        if i < len(headings):
            headings[i].insert_after(img)
        else:
            headings[-1].insert_after(img)

    for i, ifr in enumerate(iframe_html):
        if i < len(headings):
            headings[i].insert_after(ifr)
        else:
            headings[-1].insert_after(ifr)

    return str(soup)
