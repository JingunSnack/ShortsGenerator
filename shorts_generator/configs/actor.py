import yaml

from shorts_generator.configs.voice import Voice, to_voice


class Actor:
    def __init__(self, name: str, voice: Voice, traits: list[str], unique_phrases: list[str]):
        self.name = name
        self.voice = voice
        self.traits = traits
        self.unique_phrases = unique_phrases


def load_actors_from_config(config_file):
    with open(config_file) as file:
        config = yaml.safe_load(file)
        actors = [
            Actor(
                actor["name"],
                to_voice(actor["voice"]),
                actor["traits"],
                actor["unique_phrases"],
            )
            for actor in config["actors"]
        ]
        return actors
