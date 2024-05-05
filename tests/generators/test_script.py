import json
from pathlib import Path
from unittest.mock import MagicMock

from shorts_generator.configs.actor import Actor, load_actors_from_config
from shorts_generator.generators.script import (
    generate_script_file,
    generate_script_generation_prompt,
    iter_script_content,
)


def test_generate_script_file(temp_dir, mock_openai_client, actors):
    content = "Sample content for the script"
    output_file = Path(temp_dir) / "script.json"

    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=json.dumps({"script": "Generated script"})))]
    )

    generate_script_file(mock_openai_client, actors, content, output_file)

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

    output_file = Path(tmpdir) / "script.json"

    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=json.dumps({"script": "Generated script"})))]
    )

    generate_script_file(mock_openai_client, actors, content, output_file)

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

    output_file = Path(tmpdir) / "script.json"

    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=json.dumps({"script": "Generated script"})))]
    )

    generate_script_file(mock_openai_client, actors, content, output_file)

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


def test_iter_script_content():
    script_content = [
        {"Alice": "Hi"},
        {"Bob": "Hey"},
        {"Alice": "Wut up"},
    ]

    iter = iter_script_content(script_content)

    assert ("Alice", "Hi") == next(iter)
    assert ("Bob", "Hey") == next(iter)
    assert ("Alice", "Wut up") == next(iter)


def test_generate_script_generation_prompt_single_actor():
    actors = [Actor("Alice", "nova", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"])]
    prompt = generate_script_generation_prompt(actors)

    assert "*   **Name**: Alice" in prompt
    assert "*   **Traits**: enthusiastic, curious" in prompt
    assert "*   **Unique Phrases**: Wait, what?, Oh, come on" in prompt


def test_generate_script_generation_prompt_multiple_actors():
    actors = [
        Actor("Alice", "nova", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"]),
        Actor(
            "Bob",
            "echo",
            ["analytical", "reserved"],
            ["Interesting point...", "Let me think..."],
        ),
    ]
    prompt = generate_script_generation_prompt(actors)

    assert "*   **Name**: Alice" in prompt
    assert "*   **Traits**: enthusiastic, curious" in prompt
    assert "*   **Unique Phrases**: Wait, what?, Oh, come on" in prompt

    assert "*   **Name**: Bob" in prompt
    assert "*   **Traits**: analytical, reserved" in prompt
    assert "*   **Unique Phrases**: Interesting point..., Let me think..." in prompt


def test_generate_script_generation_prompt_empty_actors():
    actors = []
    prompt = generate_script_generation_prompt(actors)

    assert "Actor Descriptions" in prompt
    assert "*   **Name**:" not in prompt
    assert "*   **Traits**:" not in prompt
    assert "*   **Unique Phrases**:" not in prompt


def test_generate_script_generation_prompt_actor_with_empty_traits_and_phrases():
    actors = [Actor("Alice", "", [], [])]
    prompt = generate_script_generation_prompt(actors)

    assert "*   **Name**: Alice" in prompt
    assert "*   **Traits**: \n" in prompt
    assert "*   **Unique Phrases**: \n" in prompt
