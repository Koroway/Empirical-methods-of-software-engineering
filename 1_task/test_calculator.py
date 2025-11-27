import pytest
from calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


def test_add_standard(calc):
    assert calc.add(2, 3) == 5


def test_add_exception(calc):
    with pytest.raises(TypeError):
        calc.add(2, "three")


@pytest.mark.parametrize("a, b, expected", [
    (10, 5, 15),
    (-1, 1, 0),
    (0, 0, 0),
    (2.5, 2.5, 5.0)
])
def test_add_parameterized(calc, a, b, expected):
    assert calc.add(a, b) == expected


def test_subtract_standard(calc):
    assert calc.subtract(10, 4) == 6


def test_subtract_exception(calc):
    with pytest.raises(TypeError):
        calc.subtract("ten", 5)


@pytest.mark.parametrize("a, b, expected", [
    (10, 5, 5),
    (0, 5, -5),
    (-5, -5, 0),
    (10.5, 0.5, 10.0)
])
def test_subtract_parameterized(calc, a, b, expected):
    assert calc.subtract(a, b) == expected

def test_multiply_standard(calc):
    assert calc.multiply(3, 4) == 12


def test_multiply_exception(calc):
    with pytest.raises(TypeError):
        calc.multiply(None, 5)


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 6),
    (-2, 3, -6),
    (0, 100, 0),
    (0.5, 2, 1.0)
])
def test_multiply_parameterized(calc, a, b, expected):
    assert calc.multiply(a, b) == expected

def test_divide_standard(calc):
    assert calc.divide(10, 2) == 5


def test_divide_exception(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)

    with pytest.raises(TypeError):
        calc.divide(10, "2")


@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (9, 3, 3),
    (-10, 2, -5),
    (5, 2, 2.5)
])
def test_divide_parameterized(calc, a, b, expected):
    assert calc.divide(a, b) == expected