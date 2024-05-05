from shorts_generator.generators.actor import Actor, generate_script_generation_prompt


def test_actor_initialization():
    actor = Actor("Alice", "nova", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"])

    assert actor.name == "Alice"
    assert actor.voice == "nova"
    assert actor.traits == ["enthusiastic", "curious"]
    assert actor.unique_phrases == ["Wait, what?", "Oh, come on"]


def test_generate_script_generation_prompt_single_actor():
    actors = [Actor("Alice", "nova", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"])]
    prompt = generate_script_generation_prompt(actors)

    assert "*   **Name**: Alice" in prompt
    assert "*   **Traits**: enthusiastic, curious" in prompt
    assert "*   **Unique Phrases**: Wait, what?, Oh, come on" in prompt


def test_generate_script_generation_prompt_multiple_actors():
    actors = [
        Actor("Alice", "nova", ["enthusiastic", "curious"], ["Wait, what?", "Oh, come on"]),
        Actor(
            "Bob",
            "echo",
            ["analytical", "reserved"],
            ["Interesting point...", "Let me think..."],
        ),
    ]
    prompt = generate_script_generation_prompt(actors)

    assert "*   **Name**: Alice" in prompt
    assert "*   **Traits**: enthusiastic, curious" in prompt
    assert "*   **Unique Phrases**: Wait, what?, Oh, come on" in prompt

    assert "*   **Name**: Bob" in prompt
    assert "*   **Traits**: analytical, reserved" in prompt
    assert "*   **Unique Phrases**: Interesting point..., Let me think..." in prompt


def test_generate_script_generation_prompt_empty_actors():
    actors = []
    prompt = generate_script_generation_prompt(actors)

    assert "Actor Descriptions" in prompt
    assert "*   **Name**:" not in prompt
    assert "*   **Traits**:" not in prompt
    assert "*   **Unique Phrases**:" not in prompt


def test_generate_script_generation_prompt_actor_with_empty_traits_and_phrases():
    actors = [Actor("Alice", "", [], [])]
    prompt = generate_script_generation_prompt(actors)

    assert "*   **Name**: Alice" in prompt
    assert "*   **Traits**: \n" in prompt
    assert "*   **Unique Phrases**: \n" in prompt
