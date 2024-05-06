from pathlib import Path

import requests
from openai import OpenAI

from shorts_generator.generators.script import iter_script_content


def generate_image_file(client: OpenAI, script_content: list[dict], output_file: Path):
    content = "\n".join(
        f"{speaker}: {content}" for speaker, content in iter_script_content(script_content)
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=content,
        size="1024x1792",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    response = requests.get(image_url, timeout=5)

    output_file.write_bytes(response.content)
