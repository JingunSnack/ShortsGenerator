from enum import Enum


class Voice(Enum):
    ALLOY = "alloy"
    ECHO = "echo"
    FABLE = "fable"
    ONYX = "onyx"
    NOVA = "nova"
    SHIMMER = "shimmer"


def to_voice(voice: str) -> Voice:
    try:
        return Voice(voice.lower())
    except ValueError:
        return Voice.ALLOY
