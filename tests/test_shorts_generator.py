from unittest.mock import patch


def test_generate_script(shorts_generator):
    with patch("shorts_generator.generators.generate_script_file") as mock_generate_script_file:
        shorts_generator.workspace.content_file.write_text("Sample content")

        shorts_generator.generate_script()

        mock_generate_script_file.assert_called_once_with(
            shorts_generator.openai_client,
            shorts_generator.actors,
            shorts_generator.workspace.get_content(),
            shorts_generator.workspace.script_file,
        )


def test_generate_audio(shorts_generator, actors):
    with patch("shorts_generator.generators.generate_audio_file") as mock_generate_audio_file:
        assert actors[0].name == "Alice"
        assert actors[1].name == "Bob"

        shorts_generator.workspace.script_file.write_text(
            '{ "script": [ {"Alice": "Hi"}, {"Bob": "Hello"} ] }'
        )

        shorts_generator.generate_audio()

        assert mock_generate_audio_file.call_count == 2

        mock_generate_audio_file.assert_any_call(
            client=shorts_generator.openai_client,
            voice=actors[0].voice,
            content="Hi",
            output_file=shorts_generator.workspace.audio_dir / "000.mp3",
        )
        mock_generate_audio_file.assert_any_call(
            client=shorts_generator.openai_client,
            voice=actors[1].voice,
            content="Hello",
            output_file=shorts_generator.workspace.audio_dir / "001.mp3",
        )


def test_generate_image(shorts_generator, actors):
    with patch("shorts_generator.generators.generate_image_file") as mock_generate_image_file:
        assert actors[0].name == "Alice"
        assert actors[1].name == "Bob"

        shorts_generator.workspace.script_file.write_text(
            '{ "script": [ {"Alice": "Hi"}, {"Bob": "Hello"} ] }'
        )

        shorts_generator.generate_image()

        assert mock_generate_image_file.call_count == shorts_generator.num_images

        mock_generate_image_file.assert_any_call(
            client=shorts_generator.openai_client,
            script_content=shorts_generator.workspace.get_script_content(),
            output_file=shorts_generator.workspace.image_dir / "000.png",
        )
        mock_generate_image_file.assert_any_call(
            client=shorts_generator.openai_client,
            script_content=shorts_generator.workspace.get_script_content(),
            output_file=shorts_generator.workspace.image_dir / "001.png",
        )


def test_generate_video(shorts_generator, actors):
    with patch("shorts_generator.generators.generate_video_file") as mock_generate_video_file:
        assert actors[0].name == "Alice"
        assert actors[1].name == "Bob"

        shorts_generator.workspace.script_file.write_text(
            '{ "script": [ {"Alice": "Hi"}, {"Bob": "Hello"} ] }'
        )

        (shorts_generator.workspace.audio_dir / "000.mp3").touch()
        (shorts_generator.workspace.audio_dir / "001.mp3").touch()

        (shorts_generator.workspace.image_dir / "000.png").touch()
        (shorts_generator.workspace.image_dir / "001.png").touch()

        shorts_generator.generate_video()

        mock_generate_video_file.assert_called_once_with(
            script_content=shorts_generator.workspace.get_script_content(),
            actors_dict=shorts_generator.actors_dict,
            audio_files=shorts_generator.workspace.get_audio_files(),
            image_files=shorts_generator.workspace.get_image_files(),
            output_file=shorts_generator.workspace.video_file,
        )
