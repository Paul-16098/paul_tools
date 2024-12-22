from .__init__ import *
from ..Roll import Roll


def test_rollTextReplace():
    """
    Unit test for the rollTextReplace method of the Roll class.

    This test verifies that the rollTextReplace method correctly replaces
    specific input strings with their corresponding output strings.

    Assertions:
    - rollTextReplace("int") should return "智力 "
    - rollTextReplace("san") should return "理智 "
    - rollTextReplace("other") should return "other"
    """
    assert Roll.rollTextReplace("int") == "智力 "
    assert Roll.rollTextReplace("san") == "理智 "
    assert Roll.rollTextReplace("other") == "other"


def test_RollNumRegTools():
    """
    Test the RollNumRegTools method of the Roll class.

    This test verifies that the RollNumRegTools method correctly parses dice notation strings
    and returns the expected list of integers representing the number of dice, the type of dice,
    and any modifier.

    Assertions:
    - The method correctly parses "2d6+3" to [2, 6, 3].
    - The method correctly parses "d20" to [1, 20, 0].
    - The method raises an exception for invalid input "invalid".

    Raises:
    - Exception: If the input string is invalid.
    """
    roll = Roll()
    assert roll.RollNumRegTools("2d6+3") == [2, 6, 3]
    assert roll.RollNumRegTools("d20") == [1, 20, 0]
    with pytest.raises(Exception):
        roll.RollNumRegTools("invalid")


def test_RollNum():
    """
    Test the RollNum method of the Roll class.

    This test checks if the RollNum method correctly processes the input string "2d6+3"
    and returns a result dictionary containing the keys "rollValueList", "Type", and "returnValueList".

    Assertions:
        - The result dictionary contains the key "rollValueList".
        - The result dictionary contains the key "Type".
        - The result dictionary contains the key "returnValueList".
    """
    roll = Roll()
    result = roll.RollNum("2d6+3")
    assert "rollValueList" in result
    assert "Type" in result
    assert "returnValueList" in result


def test_RollList():
    """
    Test the RollList method of the Roll class.

    This test creates an instance of the Roll class and calls the RollList method
    with a list of integers. It asserts that the result of the RollList method
    is one of the integers in the input list.

    Returns:
        None
    """
    roll = Roll()
    result = roll.RollList([1, 2, 3, 4, 5])
    assert result in [1, 2, 3, 4, 5]


def test_getExpectedValue():
    """
    Test the getExpectedValue method of the Roll class.
    This test checks the following scenarios:
    1. The expected value is correctly calculated given a list of values and their corresponding probabilities.
    2. A ValueError is raised when the lengths of the values and probabilities lists do not match.
    3. A ValueError is raised when the sum of probabilities does not equal 1.
    Test cases:
    - values = [1, 2, 3], probabilities = [0.2, 0.5, 0.3], expected result = 2.1
    - values = [1, 2], probabilities = [0.5, 0.5, 0.1], should raise ValueError
    - values = [1, 2], probabilities = [0.5, 0.4], should raise ValueError
    """
    roll = Roll()
    values = [1, 2, 3]
    probabilities = [0.2, 0.5, 0.3]
    assert roll.getExpectedValue(values, probabilities) == pytest.approx(2.1)

    with pytest.raises(ValueError):
        roll.getExpectedValue([1, 2], [0.5, 0.5, 0.1])

    with pytest.raises(ValueError):
        roll.getExpectedValue([1, 2], [0.5, 0.4])
