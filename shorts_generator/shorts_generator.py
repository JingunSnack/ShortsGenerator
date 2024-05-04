from pathlib import Path

from openai import OpenAI

from shorts_generator.generators.actor import Actor
from shorts_generator.generators.script import generate_script_file
from shorts_generator.workspace import Workspace


class ShortsGenerator:
    def __init__(
        self,
        openai_client: OpenAI,
        actors: list[Actor],
        content_file: Path,
        workspace: Workspace,
    ):
        self.openai_client = openai_client
        self.content_file = content_file
        self.actors = actors
        self.workspace = workspace

    def generate_script(self):
        if self.workspace.has_script_file():
            return

        generate_script_file(
            self.openai_client,
            self.actors,
            self.content_file.read_text(),
            self.workspace.script_file,
        )

    def generate_audio(self):
        if self.workspace.has_audio_files():
            return
        raise NotImplementedError

    def generate_image(self):
        if self.workspace.has_image_files():
            return
        raise NotImplementedError

    def generate_video(self):
        if self.workspace.has_video_file():
            return

        self.generate_script()
        self.generate_audio()
        self.generate_image()

        raise NotImplementedError
