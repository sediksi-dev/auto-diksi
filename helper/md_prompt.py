import re


def prompt_from_md(filepath: str, **kwargs) -> str:
    with open(filepath, "r") as file:
        if kwargs:
            return file.read().format(**kwargs)
        return file.read()


def prompt_md_by_tag(filepath: str, tag: str, **kwargs) -> str:
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    pattern = f"<{tag}>(.*?)</{tag}>"
    match = re.search(pattern, content, re.DOTALL)
    if kwargs:
        return match.group(1).format(**kwargs)
    return match.group(1)
