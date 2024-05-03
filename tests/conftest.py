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
