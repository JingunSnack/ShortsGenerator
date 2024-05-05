from shorts_generator.configs.voice import Voice, to_voice


def test_to_voice():
    assert to_voice("alloy") == Voice.ALLOY
    assert to_voice("echo") == Voice.ECHO
    assert to_voice("Fable") == Voice.FABLE

    assert to_voice("onyX") == Voice.ONYX
    assert to_voice("SHIMMER") == Voice.SHIMMER

    assert to_voice("no one knows") == Voice.ALLOY
