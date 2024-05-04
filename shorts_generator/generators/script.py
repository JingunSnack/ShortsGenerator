from pathlib import Path

from openai import OpenAI

from shorts_generator.generators.actor import Actor, generate_script_generation_prompt


def _generate_script(client: OpenAI, actors: list[Actor], content: str):
    system_prompt = generate_script_generation_prompt(actors)

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": content,
            },
        ],
    )

    return response.choices[0].message.content


def generate_script_file(
    client: OpenAI, actors: list[Actor], content_file: Path, output_file: Path
):
    script = _generate_script(client, actors, content_file.read_text())

    output_file.write_text(script)
