import json
from unittest.mock import MagicMock

import pytest

from shorts_generator.generators.voice import to_voice


def test_generate_script_not_implemented(mock_openai_client, shorts_generator):
    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=json.dumps({"script": "Generated script"})))]
    )
    shorts_generator.generate_script()

    assert shorts_generator.workspace.has_script_file()


def test_generate_audio(mock_openai_client, shorts_generator):
    shorts_generator.workspace.script_file.write_text('[{"Alice": "Hi"}]')
    mock_openai_client.audio.speech.create.return_value = MagicMock(
        stream_to_file=MagicMock(return_value=None)
    )

    shorts_generator.generate_audio()

    mock_openai_client.audio.speech.create.assert_called_once_with(
        model="tts-1",
        voice=to_voice(shorts_generator.actors_dict["Alice"].voice).value,
        input="Hi",
    )


def test_generate_image_not_implemented(shorts_generator):
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_image()


def test_generate_video_not_implemented(mock_openai_client, shorts_generator):
    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content=json.dumps([{"Alice": "Hi"}])))]
    )
    mock_openai_client.audio.speech.create.return_value = MagicMock(
        stream_to_file=MagicMock(return_value=None)
    )

    with pytest.raises(NotImplementedError):
        shorts_generator.generate_video()


def test_generate_video_script_exists(mock_openai_client, shorts_generator):
    shorts_generator.workspace.script_file.write_text('[{"Alice": "Hi"}]')
    mock_openai_client.audio.speech.create.return_value = MagicMock(
        stream_to_file=MagicMock(return_value=None)
    )
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_video()


def test_generate_video_audio_exists(shorts_generator):
    shorts_generator.workspace.script_file.touch()
    audio_file = shorts_generator.workspace.audio_dir / "audio.mp3"
    audio_file.touch()
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_video()


def test_generate_video_image_exists(shorts_generator):
    shorts_generator.workspace.script_file.touch()
    audio_file = shorts_generator.workspace.audio_dir / "audio.mp3"
    audio_file.touch()
    image_file = shorts_generator.workspace.image_dir / "audio.mp3"
    image_file.touch()
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_video()
