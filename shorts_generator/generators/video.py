from pathlib import Path

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
)

from shorts_generator.configs.actor import Actor
from shorts_generator.generators import iter_script_content


def generate_video_file(
    script_content: list[dict],
    actors_dict: dict[str, Actor],
    audio_files: list[Path],
    image_files: list[Path],
    output_file: Path,
    zoom_image: bool = False,
):
    audio_clips = create_audio_clips(audio_files)
    text_clips = create_text_clips(script_content, audio_clips, actors_dict)
    image_clips = create_image_clips(
        image_files, sum(clip.duration for clip in audio_clips), zoom_image=zoom_image
    )

    CompositeVideoClip(image_clips + text_clips).set_audio(
        CompositeAudioClip(audio_clips)
    ).write_videofile(str(output_file), fps=24)


def create_audio_clips(audio_files: list[Path]):
    audio_clips = []
    offset = 0
    for file in audio_files:
        audio_clips.append(AudioFileClip(str(file)).set_start(offset))
        offset += audio_clips[-1].duration

    return audio_clips


def create_text_clips(
    script_content: list[dict],
    audio_clips: list[AudioFileClip],
    actors_dict: dict[str, Actor],
):
    text_clips = []
    for idx, (speaker, content) in enumerate(iter_script_content(script_content)):
        offset = 0
        for partial_content in _split_content(content, limit=10):
            text_clip = TextClip(
                partial_content,
                font=actors_dict[speaker].text_font,
                fontsize=actors_dict[speaker].text_font_size,
                color=actors_dict[speaker].text_color,
                stroke_color=actors_dict[speaker].text_stroke_color,
                stroke_width=actors_dict[speaker].text_stroke_width,
            )
            duration = audio_clips[idx].duration * len(partial_content) / len(content)
            text_clip = (
                text_clip.set_position("center")
                .set_start(audio_clips[idx].start + offset)
                .set_duration(duration)
            )
            text_clip = text_clip.crossfadein(0.01).crossfadeout(0.01)
            text_clips.append(text_clip)

            offset += duration

    return text_clips


def create_image_clips(image_files: list[Path], total_duration, zoom_image=False):
    duration = total_duration / len(image_files)

    if not zoom_image:
        return [
            ImageClip(str(image_file)).set_start(idx * duration).set_duration(duration)
            for idx, image_file in enumerate(image_files)
        ]

    zoom_ratio = 1.2  # TBD

    return [
        ImageClip(str(image_file))
        .set_start(idx * duration)
        .set_duration(duration)
        .resize(lambda t: 1 + (zoom_ratio - 1) * t / duration)
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
