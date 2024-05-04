import yaml


class Actor:
    def __init__(self, name, traits, unique_phrases):
        self.name = name
        self.traits = traits
        self.unique_phrases = unique_phrases


def load_actors_from_config(config_file):
    with open(config_file) as file:
        config = yaml.safe_load(file)
        actors = [
            Actor(actor["name"], actor["traits"], actor["unique_phrases"])
            for actor in config["actors"]
        ]
        return actors


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
