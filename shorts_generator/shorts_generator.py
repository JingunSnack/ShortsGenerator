from shorts_generator.workspace import Workspace


class ShortsGenerator:
    def __init__(self, workspace: Workspace):
        self.workspace = workspace

    def generate_script(self):
        if self.workspace.has_script_file():
            return
        raise NotImplementedError

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
