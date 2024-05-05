from pathlib import Path

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
)

from shorts_generator.generators import iter_script_content


def generate_video_file(
    script_content: list[dict],
    audio_files: list[Path],
    image_files: list[Path],
    output_file: Path,
):
    audio_clips = create_audio_clips(audio_files)
    text_clips = create_text_clips(script_content, audio_clips)
    image_clips = create_image_clips(image_files, sum(clip.duration for clip in audio_clips))

    CompositeVideoClip(image_clips + text_clips).set_audio(
        CompositeAudioClip(audio_clips)
    ).write_videofile(str(output_file), fps=24)


def create_audio_clips(audio_files: list[Path]):
    return [AudioFileClip(str(file)) for file in audio_files]


def create_text_clips(script_content: list[dict], audio_clips: list[AudioFileClip]):
    text_clips = []
    offset = 0
    for idx, (_, content) in enumerate(iter_script_content(script_content)):
        for partial_content in _split_content(content, limit=10):
            text_clip = TextClip(
                partial_content,
                fontsize=120,
                font="Lato-Semibold",
                color="white",
                stroke_color="black",
                stroke_width=3,
            )
            duration = audio_clips[idx].duration * len(partial_content) / len(content)
            text_clip = text_clip.set_position("center").set_start(offset).set_duration(duration)
            text_clip = text_clip.crossfadein(0.01).crossfadeout(0.01)
            text_clips.append(text_clip)

            offset += duration

    return text_clips


def create_image_clips(image_files: list[Path], total_duration):
    duration = total_duration / len(image_files)

    return [
        ImageClip(str(image_file)).set_start(idx * duration).set_duration(duration)
        for idx, image_file in enumerate(image_files)
    ]


def _split_content(content, limit):
    ret = []
    for word in content.split():
        if not ret or len(" ".join(ret[-1])) + len(word) > limit:
            ret.append([word])
        else:
            ret[-1].append(word)
    return [" ".join(words) for words in ret]
