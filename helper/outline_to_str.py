from modules.ai.tools.outline_generator import OutlineArticle


def outline_to_str(outline: OutlineArticle) -> str:
    outline_str = ""

    outline_str += "# Intro\n"
    outline_str += f"{outline.intro}\n\n"
    outline_str += "# Sections\n"
    for section in outline.sections:
        outline_str += f"## {section.subheading}\n"
        for info in section.information:
            outline_str += f"- {info}\n"
        outline_str += "\n"

    return outline_str
