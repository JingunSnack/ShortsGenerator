from pathlib import Path
from unittest.mock import MagicMock

from shorts_generator.generators.audio import generate_audio_file
from shorts_generator.generators.voice import Voice


def test_generate_audio_file(tmpdir, mock_openai_client):
    content = "Sample content for the script"
    output_file = Path(tmpdir) / "audio.mp3"

    mock_openai_client.audio.speech.create.return_value = MagicMock(
        stream_to_file=MagicMock(return_value=None)
    )

    generate_audio_file(mock_openai_client, Voice.ALLOY, content, output_file)

    mock_openai_client.audio.speech.create.assert_called_once_with(
        model="tts-1-hd", voice=Voice.ALLOY.value, input=content
    )
