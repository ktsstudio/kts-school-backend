import math

import pytest


def division(a, b):
    return a / b


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        division(100, 0)


def test_str():
    with pytest.raises(TypeError):
        division("a", "b")


@pytest.mark.parametrize(
    "a,b,expected", [[100, 20, 5], [100, -50, -2], [5, 2, 2.5], [0, 2, 0]]
)
def test_division(a, b, expected):
    assert division(a, b) == expected
