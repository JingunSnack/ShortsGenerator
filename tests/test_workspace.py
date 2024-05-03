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


def test_create_workspace(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    assert workspace_dir.exists()
    assert workspace.audio_dir.exists()
    assert workspace.image_dir.exists()
    assert workspace.workspace_content_file.exists()


def test_get_content(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    content = workspace.get_content()
    assert content == "Awesome content"


def test_script_file_path(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    assert workspace.script_file == workspace_dir / "script.json"


def test_video_file_path(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    assert workspace.video_file == workspace_dir / "video.mp4"
