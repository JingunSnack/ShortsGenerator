from openai import OpenAI

from shorts_generator.generators.actor import Actor
from shorts_generator.generators.audio import generate_audio_file
from shorts_generator.generators.image import generate_image_file
from shorts_generator.generators.script import generate_script_file
from shorts_generator.generators.util import iter_script_content, load_script_content
from shorts_generator.generators.voice import to_voice
from shorts_generator.workspace import Workspace


class ShortsGenerator:
    def __init__(
        self,
        openai_client: OpenAI,
        actors: list[Actor],
        workspace: Workspace,
    ):
        self.openai_client = openai_client
        self.actors = actors
        self.actors_dict = {actor.name: actor for actor in self.actors}
        self.workspace = workspace

    def generate_script(self):
        if self.workspace.has_script_file():
            return

        generate_script_file(
            self.openai_client,
            self.actors,
            self.workspace.get_content(),
            self.workspace.script_file,
        )

    def generate_audio(self):
        if self.workspace.has_audio_files():
            return

        script_content = load_script_content(self.workspace.script_file)

        for idx, (speaker, content) in enumerate(iter_script_content(script_content)):
            generate_audio_file(
                client=self.openai_client,
                voice=to_voice(self.actors_dict[speaker].voice),
                content=content,
                output_file=self.workspace.audio_dir / f"{idx:03}.mp3",
            )

    def generate_image(self):
        if self.workspace.has_image_files():
            return

        script_content = load_script_content(self.workspace.script_file)

        for idx, (_, content) in enumerate(iter_script_content(script_content)):
            generate_image_file(
                client=self.openai_client,
                content=content,
                output_file=self.workspace.image_dir / f"{idx:03}.png",
            )

    def generate_video(self):
        if self.workspace.has_video_file():
            return

        self.generate_script()
        self.generate_audio()
        self.generate_image()

        raise NotImplementedError
