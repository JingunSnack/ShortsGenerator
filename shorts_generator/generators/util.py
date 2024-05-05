def iter_script_content(script_content: list[dict]):
    for line in script_content:
        yield from line.items()
