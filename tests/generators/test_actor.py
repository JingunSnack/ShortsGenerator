from shorts_generator.generators.actor import Actor, generate_script_generation_prompt


def test_actor_initialization():
    actor = Actor("Alice", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"])

    assert actor.name == "Alice"
    assert actor.traits == ["enthusiastic", "curious"]
    assert actor.unique_phrases == ["Wait, what?", "Oh, come on"]


def test_generate_script_generation_prompt_single_actor():
    actors = [Actor("Alice", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"])]
    prompt = generate_script_generation_prompt(actors)

    assert "Alice" in prompt
    assert "enthusiastic" in prompt
    assert "curious" in prompt
    assert "Wait, what?" in prompt
    assert "Oh, come on" in prompt


def test_generate_script_generation_prompt_multiple_actors():
    actors = [
        Actor("Alice", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"]),
        Actor(
            "Bob",
            ["analytical", "reserved"],
            ["Interesting point...", "Let me think..."],
        ),
    ]
    prompt = generate_script_generation_prompt(actors)

    assert "Alice" in prompt
    assert "enthusiastic" in prompt
    assert "curious" in prompt
    assert "Wait, what?" in prompt
    assert "Oh, come on" in prompt
    assert "Bob" in prompt
    assert "analytical" in prompt
    assert "reserved" in prompt
    assert "Interesting point..." in prompt
    assert "Let me think..." in prompt


def test_generate_script_generation_prompt_empty_actors():
    actors = []
    prompt = generate_script_generation_prompt(actors)

    assert "Actor Descriptions" in prompt
    assert "The script should be easy to follow" in prompt


def test_generate_script_generation_prompt_actor_with_empty_traits_and_phrases():
    actors = [Actor("Alice", [], [])]
    prompt = generate_script_generation_prompt(actors)

    assert "Alice" in prompt
    assert "**Traits**:" in prompt
    assert "**Unique Phrases**:" in prompt
