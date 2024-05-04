import json
from pathlib import Path
from unittest.mock import MagicMock

from shorts_generator.generators.actor import Actor, load_actors_from_config
from shorts_generator.generators.script import generate_script_file


def test_generate_script_file(tmpdir, mock_openai_client):
    actors = [
        Actor("Alice", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"]),
        Actor(
            "Bob",
            ["analytical", "reserved"],
            ["Interesting point...", "Let me think..."],
        ),
    ]
    content = "Sample content for the script"
    content_file = Path(tmpdir) / "content.txt"
    content_file.write_text(content)

    output_file = Path(tmpdir) / "script.json"

    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=json.dumps({"script": "Generated script"})))]
    )

    generate_script_file(mock_openai_client, actors, content_file, output_file)

    assert output_file.read_text() == '{"script": "Generated script"}'

    mock_openai_client.chat.completions.create.assert_called_once_with(
        model="gpt-4-turbo",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": mock_openai_client.chat.completions.create.call_args[1]["messages"][0][
                    "content"
                ],
            },
            {"role": "user", "content": content},
        ],
    )


def test_generate_script_file_actor_config(tmpdir, mock_openai_client):
    config_file = "actor_config_example.yaml"
    actors = load_actors_from_config(config_file)
    content = "Sample content for the script"
    content_file = Path(tmpdir) / "content.txt"
    content_file.write_text(content)

    output_file = Path(tmpdir) / "script.json"

    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=json.dumps({"script": "Generated script"})))]
    )

    generate_script_file(mock_openai_client, actors, content_file, output_file)

    assert output_file.read_text() == '{"script": "Generated script"}'

    mock_openai_client.chat.completions.create.assert_called_once_with(
        model="gpt-4-turbo",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": mock_openai_client.chat.completions.create.call_args[1]["messages"][0][
                    "content"
                ],
            },
            {"role": "user", "content": content},
        ],
    )


def test_generate_script_file_empty_actors(tmpdir, mock_openai_client):
    actors = []
    content = "Sample content for the script"
    content_file = Path(tmpdir) / "content.txt"
    content_file.write_text(content)

    output_file = Path(tmpdir) / "script.json"

    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=json.dumps({"script": "Generated script"})))]
    )

    generate_script_file(mock_openai_client, actors, content_file, output_file)

    assert output_file.read_text() == '{"script": "Generated script"}'

    mock_openai_client.chat.completions.create.assert_called_once()
