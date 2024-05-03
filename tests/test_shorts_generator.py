import pytest

from shorts_generator.shorts_generator import ShortsGenerator


def test_generate_script_not_implemented(workspace):
    shorts_generator = ShortsGenerator(workspace)
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_script()


def test_generate_audio_not_implemented(workspace):
    shorts_generator = ShortsGenerator(workspace)
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_audio()


def test_generate_image_not_implemented(workspace):
    shorts_generator = ShortsGenerator(workspace)
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_image()


def test_generate_video_not_implemented(workspace):
    shorts_generator = ShortsGenerator(workspace)
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_video()


def test_generate_video_script_exists(workspace):
    workspace.script_file.touch()
    shorts_generator = ShortsGenerator(workspace)
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_video()


def test_generate_video_audio_exists(workspace):
    workspace.script_file.touch()
    audio_file = workspace.audio_dir / "audio.mp3"
    audio_file.touch()
    shorts_generator = ShortsGenerator(workspace)
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_video()


def test_generate_video_image_exists(workspace):
    workspace.script_file.touch()
    audio_file = workspace.audio_dir / "audio.mp3"
    audio_file.touch()
    image_file = workspace.image_dir / "image.png"
    image_file.touch()
    shorts_generator = ShortsGenerator(workspace)
    with pytest.raises(NotImplementedError):
        shorts_generator.generate_video()
