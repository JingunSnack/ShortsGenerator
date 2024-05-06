from pathlib import Path

from moviepy.editor import AudioFileClip, ImageClip, TextClip

from shorts_generator.generators import iter_script_content
from shorts_generator.generators.video import (
    _split_content,
    create_audio_clips,
    create_image_clips,
    create_text_clips,
    generate_video_file,
)


def test_create_audio_clips():
    tests_dir = Path(__file__).resolve().parent.parent

    audio_files = [
        tests_dir / "samples" / "audio" / "000.mp3",
        tests_dir / "samples" / "audio" / "001.mp3",
    ]

    audio_clips = create_audio_clips(audio_files)

    assert len(audio_clips) == len(audio_files)

    for audio_clip, audio_file in zip(audio_clips, audio_files):
        assert isinstance(audio_clip, AudioFileClip)
        assert audio_clip.filename == str(audio_file)
        assert audio_clip.duration > 0


def test_create_image_clips():
    tests_dir = Path(__file__).resolve().parent.parent

    image_files = [
        tests_dir / "samples" / "image" / "000.png",
        tests_dir / "samples" / "image" / "001.png",
    ]

    total_duration = 10

    image_clips = create_image_clips(image_files, total_duration)

    assert len(image_clips) == len(image_files)

    for idx, image_clip in enumerate(image_clips):
        assert isinstance(image_clip, ImageClip)
        assert image_clip.start == idx * (total_duration / len(image_files))
        assert image_clip.duration == total_duration / len(image_files)
        assert image_clip.end == (idx + 1) * (total_duration / len(image_files))


def test_create_text_clips():
    script_content = [
        {
            "Alice": (
                "Wait, what? Someone sneaked a backdoor into XZ Utils, "
                "that compression thing on Linux?"
            )
        },
        {
            "Bob": (
                "TRUE. It happened in the latest versions, 5.6.0 and 5.6.1. "
                "Allows hackers to run malicious code."
            )
        },
    ]
    tests_dir = Path(__file__).resolve().parent.parent

    audio_files = [
        tests_dir / "samples" / "audio" / "000.mp3",
        tests_dir / "samples" / "audio" / "001.mp3",
    ]

    audio_clips = create_audio_clips(audio_files)

    text_clips = create_text_clips(script_content, audio_clips)

    assert len(text_clips) == sum(
        len(_split_content(content, limit=10)) for _, content in iter_script_content(script_content)
    )

    for idx, (_, content) in enumerate(iter_script_content(script_content)):
        offset = 0
        for partial_content in _split_content(content, limit=10):
            text_clip = [
                clip for clip in text_clips if clip.start == audio_clips[idx].start + offset
            ][0]

            assert isinstance(text_clip, TextClip)
            assert text_clip.start == audio_clips[idx].start + offset
            assert text_clip.duration == audio_clips[idx].duration * len(partial_content) / len(
                content
            )

            offset += text_clip.duration


def test_generate_video_file(temp_dir):
    script_content = [
        {
            "Alice": (
                "Wait, what? Someone sneaked a backdoor into XZ Utils, "
                "that compression thing on Linux?"
            )
        },
        {
            "Bob": (
                "TRUE. It happened in the latest versions, 5.6.0 and 5.6.1. "
                "Allows hackers to run malicious code."
            )
        },
    ]
    tests_dir = Path(__file__).resolve().parent.parent

    audio_files = [
        tests_dir / "samples" / "audio" / "000.mp3",
        tests_dir / "samples" / "audio" / "001.mp3",
    ]

    image_files = [
        tests_dir / "samples" / "image" / "000.png",
        tests_dir / "samples" / "image" / "001.png",
    ]

    output_file = temp_dir / "video.mp4"

    generate_video_file(
        script_content=script_content,
        audio_files=audio_files,
        image_files=image_files,
        output_file=output_file,
    )

    assert output_file.exists()


def test_split_content():
    content1 = "This is a sample content."
    limit1 = 10
    expected_output1 = ["This is a", "sample", "content."]
    assert _split_content(content1, limit1) == expected_output1

    content2 = "Thiswordislongerthanthespecifiedlimit."
    limit2 = 10
    expected_output2 = ["Thiswordislongerthanthespecifiedlimit."]
    assert _split_content(content2, limit2) == expected_output2

    content3 = "Exactly ten Exactly ten"
    limit3 = 10
    expected_output3 = ["Exactly ten", "Exactly ten"]
    assert _split_content(content3, limit3) == expected_output3
