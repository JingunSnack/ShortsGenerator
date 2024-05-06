from shorts_generator.configs.actor import Actor
from shorts_generator.configs.voice import Voice


def test_actor_initialization():
    actor = Actor("Alice", "nova", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"])

    assert actor.name == "Alice"
    assert actor.voice == "nova"
    assert actor.traits == ["enthusiastic", "curious"]
    assert actor.unique_phrases == ["Wait, what?", "Oh, come on"]


def test_actor_from_dict():
    actor_dict = {
        "name": "Alice",
        "voice": "nova",
        "traits": ["enthusiastic", "curious"],
        "unique_phrases": ["Wait, what?", "Oh, come on"],
        "text_font": "Arial-Black",
        "text_font_size": 135,
        "text_color": "yellow",
        "text_stroke_color": "blue",
        "text_stroke_width": 5,
    }

    actor = Actor.from_dict(actor_dict)

    assert actor.name == "Alice"
    assert actor.voice == Voice.NOVA
    assert actor.traits == ["enthusiastic", "curious"]
    assert actor.unique_phrases == ["Wait, what?", "Oh, come on"]
    assert actor.text_font == "Arial-Black"
    assert actor.text_font_size == 135
    assert actor.text_color == "yellow"
    assert actor.text_stroke_color == "blue"
    assert actor.text_stroke_width == 5
