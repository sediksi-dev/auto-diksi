def prompt_from_md(filepath: str, **kwargs) -> str:
    with open(filepath, "r") as file:
        return file.read().format(**kwargs)
