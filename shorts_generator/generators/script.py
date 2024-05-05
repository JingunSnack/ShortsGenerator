from pathlib import Path

from openai import OpenAI

from shorts_generator.configs.actor import Actor


def generate_script_generation_prompt(actors):
    prompt = """\
You are an AI script generator designed to create engaging and concise scripts for YouTube Shorts \
in a structured JSON format. Your task is to develop scripts that can range from monologues for \
a single actor to dialogues involving multiple actors.

**Actor Descriptions**:
"""

    for actor in actors:
        prompt += f"""
*   **{actor.name}**:
    *   **Name**: {actor.name}
    *   **Traits**: {", ".join(actor.traits)}
    *   **Unique Phrases**: {", ".join(actor.unique_phrases)}
"""

    prompt += """
The script should be easy to follow, informative, and engaging to the audience while being concise\
enough to fit within a 60-second video. Use simple language, avoid complex jargon, and focus on \
the most essential points. Aim for a script length of around 80-100 words. Output the script as \
a JSON-parsable list of dictionaries, where each dictionary represents a line of dialogue with the \
character name as the key and their line as the value. Do not include any additional text or \
explanations in the output.
"""

    return prompt


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


def generate_script_file(client: OpenAI, actors: list[Actor], content: str, output_file: Path):
    script = _generate_script(client, actors, content)

    output_file.write_text(script)


def iter_script_content(script_content: list[dict]):
    for line in script_content:
        yield from line.items()
