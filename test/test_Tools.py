from _pytest.compat import LEGACY_PATH
from pytest import MonkeyPatch
from .__init__ import *
from ..Tools import *
import json
import os
import pyperclip


@pytest.mark.skip(reason="This test is not yet implemented.")
def test_JsonEdit(monkeypatch: MonkeyPatch, tmpdir: LEGACY_PATH):
    """
    Test the JsonEdit function.
    """

    # Create a temporary directory for the JSON file
    temp_dir = tmpdir.mkdir("json_test")
    json_file = os.path.join(temp_dir, "test.json")

    # Mock input to simulate user interaction
    inputs = iter(["key1=value1", "key2=value2", "save",
                  "key1", "del key1", "save", "EOF"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Run the JsonEdit function
    JsonEdit(name=str(json_file).replace(".json", ""))

    # Verify the contents of the JSON file
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["key2"] == "value2"
        assert "key1" not in data


def test_color():
    """
    Test the color function.
    """
    assert color("Hello", "World", color="red") == [
        '\x1b[31m', 'Hello', 'World', '\x1b[39m']
    assert color("Hello", "World") == ["Hello", "World"]
    with pytest.raises(ValueError):
        color("Hello", "World", color="invalid_color")


def test_typeToColor():
    """
    Test the typeToColor function.
    """
    assert typeToColor("ERROR") == "RED"
    assert typeToColor("ERR") == "RED"
    assert typeToColor("WARN") == "YELLOW"
    assert typeToColor("WARNING") == "YELLOW"
    assert typeToColor("info") == "INFO"


def test_clipboard(monkeypatch: MonkeyPatch):
    """
    Test the clipboard class.
    """

    # Mock pyperclip functions
    monkeypatch.setattr(pyperclip, "copy", lambda text: None)
    monkeypatch.setattr(pyperclip, "paste", lambda: "mocked text")

    clipboard.copy_to_clipboard("test text")
    assert clipboard.paste_from_clipboard() == "mocked text"


@pytest.mark.skip(reason="This test is not yet implemented.")
def test_use():
    """
    Test the use function.
    """
    global var1, var2
    var1 = None
    var2 = None

    obj = {'var1': 10, 'var2': 'hello'}
    use(obj)

    assert globals()["var1"] == 10
    assert globals()["var2"] == 'hello'
