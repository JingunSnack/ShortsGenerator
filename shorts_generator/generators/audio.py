from pathlib import Path

from openai import OpenAI

from shorts_generator.generators.voice import Voice


def generate_audio_file(client: OpenAI, voice: Voice, content: str, output_file: Path):
    response = client.audio.speech.create(model="tts-1-hd", voice=voice.value, input=content)
    response.stream_to_file(output_file)
