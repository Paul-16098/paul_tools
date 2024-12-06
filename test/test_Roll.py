from .__init__ import *


class RollTest(unittest.TestCase):
    def test_seed(self):
        from ..Roll import Roll

        seed = 1
        t = "3d75+2"
        # t = ""

        roll_obj1 = Roll(seed=seed, isLog=True)
        r1_r = roll_obj1.RollNum(t, success=20)

        roll_obj2 = Roll(seed=seed, isLog=True)
        r2_r = roll_obj2.RollNum(t)
        self.assertEqual(r1_r, r2_r)

    def test_RollList(self):
        from ..Roll import Roll
        roll_obj = Roll(isLog=True)
        r = roll_obj.RollList(
            ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10"])
        print(r)
