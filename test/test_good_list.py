from .__init__ import *
from paul_tools.good_list import list


def test_join():
    assert list(["a", "b", "c"]).join(",") == "a,b,c"
