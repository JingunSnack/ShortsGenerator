from shorts_generator.configs.actor import Actor


def test_actor_initialization():
    actor = Actor("Alice", "nova", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"])

    assert actor.name == "Alice"
    assert actor.voice == "nova"
    assert actor.traits == ["enthusiastic", "curious"]
    assert actor.unique_phrases == ["Wait, what?", "Oh, come on"]
