from .__init__ import *
from ..Decorator import getTime, noPrint, retry


# @unittest.skip("")
class DecoratorTest(unittest.TestCase):
    @retry.retry()
    @unittest.expectedFailure
    def test_decorator1(self):
        print("abc1")
        raise Exception("abc2")

    @getTime.getTime
    def test_decorator2(self):
        from time import sleep
        print("abc3-1")
        sleep(.01)
        print("abc3-2")
        sleep(.02)

    @noPrint.noPrint
    def test_decorator3(self):
        print("abc")
