from pydantic import BaseModel
from typing import List
from modules.ai.models import KeywordToArticleInput, KeywordToArticleOutput
from modules.ai.tasks.create_headings_from_keyword import create_headings_from_keyword
from modules.ai.tasks.create_seo_data import create_seo_data, CreateSEODataArgs
from modules.ai.tasks.create_intro import create_intro, CreateIntroArgs
from modules.ai.tasks.create_section_paragraphs import (
    create_section_paragraphs,
    CreateSectionParagraphArgs,
)
from modules.ai.tasks.add_image_to_text import add_image_to_text


class InformationItem(BaseModel):
    subheading: str
    informations: List[str]


class Informations(BaseModel):
    sections: List[InformationItem]


def seeder_default_rewriter(args: KeywordToArticleInput):
    keyword = args.keyword
    lang_target = args.lang_target
    outline = create_headings_from_keyword(keyword, lang_target)
    try:
        outline = Informations.model_validate(outline)
    except Exception as e:
        raise ValueError(f"outline doesn't have the correct format: {e}")
    outline_str = ""
    for section in outline.sections:
        outline_str += f"\n## {section.subheading}\n"
        for info in section.informations:
            outline_str += f"\n{info}\n"

    seo_data = create_seo_data(
        args=CreateSEODataArgs(
            lang_target=lang_target,
            outline=outline_str,
        )
    )

    intro = create_intro(
        args=CreateIntroArgs(
            keyword=keyword,
            title=seo_data.seo_title,
            description=seo_data.meta_description,
            lang_target=lang_target,
            intent=seo_data.intent,
            style=seo_data.style,
            tone=seo_data.tone,
        )
    )

    outline_str_headline = "\n".join(
        [f"- {section.subheading}" for section in outline.sections]
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
                informations=section.informations,
            ),
            mode="long",
        )
        try:
            result = add_image_to_text(paragraph)
        except Exception:
            print("Error adding image to text")
            result = paragraph
            continue

        body_text.append(result)

    full_article = intro + "\n" + "\n".join(body_text)

    return KeywordToArticleOutput(
        title=seo_data.seo_title,
        description=seo_data.meta_description,
        keyword=keyword,
        article=full_article,
    )
