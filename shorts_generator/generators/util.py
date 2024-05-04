import json
from pathlib import Path


def load_script_content(script_file: Path) -> list[dict]:
    script_content = script_file.read_text()
    return json.loads(script_content)


def iter_script_content(script_content: list[dict]):
    for line in script_content:
        yield from line.items()
