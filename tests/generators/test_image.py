from pathlib import Path
from unittest.mock import MagicMock

import requests_mock

from shorts_generator.generators import generate_image_file


def test_generate_image_file(temp_dir, mock_openai_client):
    content = "Sample content for the script"
    output_file = Path(temp_dir) / "image.png"

    mock_openai_client.images.generate.return_value = MagicMock(
        data=[MagicMock(url="http://dummy-image-url")]
    )

    with requests_mock.Mocker() as mock_requests:
        mock_requests.get("http://dummy-image-url", content=b"dummy image content")

        generate_image_file(mock_openai_client, content, output_file)

    mock_openai_client.images.generate.assert_called_once_with(
        model="dall-e-2",
        prompt=content,
        size="256x256",
        quality="standard",
        n=1,
    )

    assert output_file.exists()
    assert output_file.read_bytes() == b"dummy image content"
