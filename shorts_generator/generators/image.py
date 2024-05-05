from pathlib import Path

import requests
from openai import OpenAI


def generate_image_file(client: OpenAI, content: str, output_file: Path):
    response = client.images.generate(
        model="dall-e-2",
        prompt=content,
        size="256x256",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    response = requests.get(image_url, timeout=5)

    output_file.write_bytes(response.content)
