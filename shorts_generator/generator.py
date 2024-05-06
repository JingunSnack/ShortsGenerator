from openai import OpenAI

from shorts_generator import generators
from shorts_generator.configs.actor import Actor
from shorts_generator.workspace import Workspace


class ShortsGenerator:
    def __init__(
        self,
        openai_client: OpenAI,
        actors: list[Actor],
        workspace: Workspace,
        num_images: int = 2,
    ):
        self.openai_client = openai_client
        self.actors = actors
        self.actors_dict = {actor.name: actor for actor in self.actors}
        self.workspace = workspace
        self.num_images = num_images

    def generate_script(self):
        if self.workspace.has_script_file():
            return

        generators.generate_script_file(
            self.openai_client,
            self.actors,
            self.workspace.get_content(),
            self.workspace.script_file,
        )

    def generate_audio(self):
        if self.workspace.has_audio_files():
            return

        for idx, (speaker, content) in enumerate(
            generators.iter_script_content(self.workspace.get_script_content())
        ):
            generators.generate_audio_file(
                client=self.openai_client,
                voice=self.actors_dict[speaker].voice,
                content=content,
                output_file=self.workspace.audio_dir / f"{idx:03}.mp3",
            )

    def generate_image(self):
        if self.workspace.has_image_files():
            return

        for idx in range(self.num_images):
            generators.generate_image_file(
                client=self.openai_client,
                script_content=self.workspace.get_script_content(),
                output_file=self.workspace.image_dir / f"{idx:03}.png",
            )

    def generate_video(self):
        if self.workspace.has_video_file():
            return

        self.generate_script()
        self.generate_audio()
        self.generate_image()

        generators.generate_video_file(
            script_content=self.workspace.get_script_content(),
            actors_dict=self.actors_dict,
            audio_files=self.workspace.get_audio_files(),
            image_files=self.workspace.get_image_files(),
            output_file=self.workspace.video_file,
        )
