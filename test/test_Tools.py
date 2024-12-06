from .__init__ import *


# @unittest.skip("")
class ToolsTest(unittest.TestCase):
    def test_color(self):
        from ..Tools import color
        print(*color("color:RED", color="RED"))
