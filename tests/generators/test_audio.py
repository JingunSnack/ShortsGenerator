from pathlib import Path
from unittest.mock import MagicMock

from shorts_generator.configs.voice import Voice
from shorts_generator.generators.audio import generate_audio_file


def test_generate_audio_file(temp_dir, mock_openai_client):
    content = "Sample content for the script"
    output_file = Path(temp_dir) / "audio.mp3"

    mock_openai_client.audio.speech.create.return_value = MagicMock(
        stream_to_file=MagicMock(return_value=None)
    )

    generate_audio_file(mock_openai_client, Voice.ALLOY, content, output_file)

    mock_openai_client.audio.speech.create.assert_called_once_with(
        model="tts-1-hd", voice=Voice.ALLOY.value, input=content
    )
