from pathlib import Path

from shorts_generator.generators.util import iter_script_content, load_script_content


def test_load_script_content(temp_dir):
    script_file = Path(temp_dir) / "script.json"
    script_file.write_text('[{"Alice": "hi"}]')

    assert load_script_content(script_file) == [{"Alice": "hi"}]


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
