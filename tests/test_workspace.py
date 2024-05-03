import shutil
import tempfile
from pathlib import Path

import pytest

from shorts_generator.workspace import Workspace


@pytest.fixture
def temp_dir():
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def content_file(temp_dir):
    content_file = temp_dir / "content.txt"
    content_file.write_text("Awesome content")
    return content_file


@pytest.fixture
def workspace(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    return Workspace(content_file, workspace_dir)


def test_create_workspace(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    assert workspace_dir.exists()
    assert workspace.audio_dir.exists()
    assert workspace.image_dir.exists()
    assert workspace.workspace_content_file.exists()


def test_script_file_path(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    assert workspace.script_file == workspace_dir / "script.json"


def test_video_file_path(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    assert workspace.video_file == workspace_dir / "video.mp4"


def test_get_content(workspace):
    content = workspace.get_content()
    assert content == "Awesome content"


def test_has_script_file(workspace):
    assert not workspace.has_script_file()

    workspace.script_file.touch()
    assert workspace.has_script_file()


def test_has_audio_files(workspace):
    assert not workspace.has_audio_files()

    audio_file = workspace.audio_dir / "audio1.mp3"
    audio_file.touch()
    assert workspace.has_audio_files()


def test_has_image_files(workspace):
    assert not workspace.has_image_files()

    image_file = workspace.image_dir / "image1.png"
    image_file.touch()
    assert workspace.has_image_files()


def test_has_video_file(workspace):
    assert not workspace.has_video_file()

    workspace.video_file.touch()
    assert workspace.has_video_file()
