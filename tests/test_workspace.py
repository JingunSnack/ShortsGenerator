from shorts_generator.workspace import Workspace


def test_create_workspace(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    assert workspace_dir.exists()
    assert workspace.audio_dir.exists()
    assert workspace.image_dir.exists()
    assert workspace.workspace_content_file.exists()


def test_script_file_path(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    assert workspace.script_file == workspace_dir / "script.json"


def test_video_file_path(temp_dir, content_file):
    workspace_dir = temp_dir / "workspace"
    workspace = Workspace(content_file, workspace_dir)

    assert workspace.video_file == workspace_dir / "video.mp4"


def test_get_content(workspace):
    content = workspace.get_content()
    assert content == "Awesome content"


def test_has_script_file(workspace):
    assert not workspace.has_script_file()

    workspace.script_file.touch()
    assert workspace.has_script_file()


def test_get_script_content(workspace):
    workspace.script_file.write_text('[{"Alice": "Hi"}]')

    assert workspace.get_script_content() == [{"Alice": "Hi"}]


def test_has_audio_files(workspace):
    assert not workspace.has_audio_files()

    audio_file = workspace.audio_dir / "audio1.mp3"
    audio_file.touch()
    assert workspace.has_audio_files()


def test_get_audio_files(workspace):
    audio_file1 = workspace.audio_dir / "000.mp3"
    audio_file2 = workspace.audio_dir / "001.mp3"
    audio_file3 = workspace.audio_dir / "002.mp3"

    audio_file1.touch()
    audio_file2.touch()
    audio_file3.touch()

    assert workspace.get_audio_files() == [audio_file1, audio_file2, audio_file3]


def test_has_image_files(workspace):
    assert not workspace.has_image_files()

    image_file = workspace.image_dir / "image1.png"
    image_file.touch()
    assert workspace.has_image_files()


def test_get_image_files(workspace):
    image_file1 = workspace.image_dir / "000.png"
    image_file2 = workspace.image_dir / "001.png"
    image_file3 = workspace.image_dir / "002.png"

    image_file1.touch()
    image_file2.touch()
    image_file3.touch()

    assert workspace.get_image_files() == [image_file1, image_file2, image_file3]


def test_has_video_file(workspace):
    assert not workspace.has_video_file()

    workspace.video_file.touch()
    assert workspace.has_video_file()
