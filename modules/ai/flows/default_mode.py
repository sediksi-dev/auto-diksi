from modules.ai.models import ArticleToArticleInput, ArticleToArticleOutput

from modules.ai.tasks.create_seo_data import create_seo_data, CreateSEODataArgs
from modules.ai.tasks.create_intro import create_intro, CreateIntroArgs
from modules.ai.tasks.create_section_paragraphs import (
    create_section_paragraphs,
    CreateSectionParagraphArgs,
)

from modules.ai.tasks.create_outline_from_facts import (
    create_outline_from_facts,
    CreateArticleFromFacts,
)

from modules.ai.tasks.extract_info import extract_info

from helper.outline_to_str import outline_to_str


def default_rewriter(args: ArticleToArticleInput):
    """
    The flow of this mode is:
    1. Fetch original article
    2. Generate list of facts from original article
    3. Create outline from list of facts
    4. Create SEO data from outline
    5. Create intro from outline
    6. Create section paragraphs from outline
    """

    # 1. Fetch original article
    original_article = args.original_article
    lang_target = args.lang_target
    lang_source = args.lang_source

    informations = extract_info(original_article=original_article)
    outline = create_outline_from_facts(
        args=CreateArticleFromFacts(
            informations=informations,
            lang_target=lang_target,
            lang_source=lang_source,
        )
    )

    outline_str = outline_to_str(outline)
    outline_str_headline = "\n".join(
        [f"- {section.subheading}" for section in outline.sections]
    )
    seo_data = create_seo_data(
        args=CreateSEODataArgs(
            lang_target=lang_target,
            outline=outline_str,
        )
    )
    intro = create_intro(
        args=CreateIntroArgs(
            title=seo_data.seo_title,
            description=seo_data.meta_description,
            intent=seo_data.intent,
            tone=seo_data.tone,
            style=seo_data.style,
            keyword=seo_data.keyword,
            lang_target=lang_target,
            intro_guideline=outline.intro,
        )
    )

    body_text = []
    for section in outline.sections:
        paragraph = create_section_paragraphs(
            args=CreateSectionParagraphArgs(
                outline=outline_str_headline,
                intro=intro,
                lang_target=lang_target,
                keyword=seo_data.keyword,
                title=seo_data.seo_title,
                target_audience=seo_data.target_audience,
                intent=seo_data.intent,
                style=seo_data.style,
                tone=seo_data.tone,
                section_title=section.subheading,
                informations=section.information,
            )
        )
        body_text.append(paragraph)
        full_article = intro + "\n" + "\n".join(body_text)

    return ArticleToArticleOutput(
        title=seo_data.seo_title,
        description=seo_data.meta_description,
        keyword=seo_data.keyword,
        article=full_article,
    )
