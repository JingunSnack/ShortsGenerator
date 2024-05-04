import shutil
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from shorts_generator.generator import ShortsGenerator
from shorts_generator.generators.actor import Actor
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


@pytest.fixture
def mock_openai_client():
    with patch("openai.OpenAI") as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        yield mock_client


@pytest.fixture
def actors():
    return [
        Actor("Alice", "nova", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"]),
        Actor(
            "Bob",
            "echo",
            ["analytical", "reserved"],
            ["Interesting point...", "Let me think..."],
        ),
    ]


@pytest.fixture
def shorts_generator(mock_openai_client, actors, content_file, workspace):
    return ShortsGenerator(mock_openai_client, actors, content_file, workspace)
