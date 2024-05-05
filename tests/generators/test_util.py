from shorts_generator.generators.util import iter_script_content


def test_iter_script_content():
    script_content = [
        {"Alice": "Hi"},
        {"Bob": "Hey"},
        {"Alice": "Wut up"},
    ]

    iter = iter_script_content(script_content)

    assert ("Alice", "Hi") == next(iter)
    assert ("Bob", "Hey") == next(iter)
    assert ("Alice", "Wut up") == next(iter)
