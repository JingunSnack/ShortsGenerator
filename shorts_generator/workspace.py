import json
import shutil
from pathlib import Path


class Workspace:
    def __init__(self, content_file, workspace_dir):
        self.content_file = Path(content_file)
        self.workspace_dir = Path(workspace_dir)

        self.workspace_content_file = self.workspace_dir / "content.txt"
        self.script_file = self.workspace_dir / "script.json"
        self.audio_dir = self.workspace_dir / "audio"
        self.image_dir = self.workspace_dir / "image"
        self.video_file = self.workspace_dir / "video.mp4"

        self._create_workspace()

    def _create_workspace(self):
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.image_dir.mkdir(parents=True, exist_ok=True)

        shutil.copy2(self.content_file, self.workspace_content_file)

    def get_content(self):
        return self.workspace_content_file.read_text()

    def has_script_file(self):
        return self.script_file.exists()

    def get_script_content(self):
        script_content = self.script_file.read_text()
        return json.loads(script_content)

    def has_audio_files(self):
        return any(self.audio_dir.rglob("*.mp3"))

    def get_audio_files(self):
        return sorted(self.audio_dir.rglob("*.mp3"))

    def has_image_files(self):
        return any(self.image_dir.rglob("*.png"))

    def get_image_files(self):
        return sorted(self.image_dir.rglob("*.png"))

    def has_video_file(self):
        return self.video_file.exists()
