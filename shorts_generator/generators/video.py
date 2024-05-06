from pathlib import Path

from moviepy.audio.fx.volumex import volumex
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
    bgm_file: Path | None = None,
):
    audio_clips = create_audio_clips(audio_files)
    text_clips = create_text_clips(script_content, audio_clips, actors_dict)

    total_duration = sum(clip.duration for clip in audio_clips)

    image_clips = create_image_clips(image_files, total_duration, zoom_image=zoom_image)

    if bgm_file:
        audio_clips.append(
            AudioFileClip(str(bgm_file)).fx(volumex, 0.05).set_duration(total_duration)
        )

    video_clip = CompositeVideoClip(image_clips + text_clips).set_audio(
        CompositeAudioClip(audio_clips)
    )

    if video_clip.duration >= 60:
        video_clip = video_clip.speedx(factor=video_clip.duration / 59.5)

    video_clip.write_videofile(str(output_file), fps=24)


def create_audio_clips(audio_files: list[Path]) -> list[AudioFileClip]:
    audio_clips = []
    offset = 0
    for file in audio_files:
        audio_clips.append(AudioFileClip(str(file)).fx(volumex, 1.5).set_start(offset))
        offset += audio_clips[-1].duration

    return audio_clips


def create_text_clips(
    script_content: list[dict],
    audio_clips: list[AudioFileClip],
    actors_dict: dict[str, Actor],
) -> list[TextClip]:
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


def create_image_clips(
    image_files: list[Path], total_duration, zoom_image=False
) -> list[ImageClip]:
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
