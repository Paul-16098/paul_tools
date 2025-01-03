from pytest import MonkeyPatch
from .__init__ import *
from ..Tools import *
import pyperclip


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
