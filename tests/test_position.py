from Position import Position
from tests.helpers import almost_equal
import pytest


@pytest.mark.parametrize("oper, x1, y1, x2, y2, x_exp, y_exp", [
    ("+", 1, 2, 5, 16, 6, 18),
    ("+", 0, 0, 4, 7, 4, 7),
    ("+", 17, 5, -2, 1, 15, 6),
    ("+", -4, -6 , -5, -11, -9, -17),
    ("-", 10, 12, 3, 1, 7, 11),
    ("-", -4, -8, 2, -6, -6, -2),
    pytest.param("+", 3, -2, 1, 4, 4, 1, marks=pytest.mark.xfail(reason="This test is expected to fail")),
    pytest.param("-", 4, 5, 1, 4, 3, 2, marks=pytest.mark.xfail(reason="This test is expected to fail"))
])
def test_position_addition(oper, x1, y1, x2, y2, x_exp, y_exp):
    pos_1 = Position(x1, y1)
    pos_2 = Position(x2, y2)
    if oper == "+":
        pos_3 = pos_1 + pos_2
    elif oper == "-":
        pos_3 = pos_1 - pos_2
    else:
        raise Exception("Unsupported sign")
    assert pos_3.x == x_exp and pos_3.y == y_exp
    assert pos_3[0] == x_exp and pos_3[1] == y_exp
    assert pos_3 == Position(x_exp, y_exp)
    assert pos_3 == [x_exp, y_exp]


@pytest.mark.parametrize("x1, y1, multipler, expect", [
    (1, 2, 4, Position(4, 8)),
    (1, 2, 4, [4, 8]),
    (0, 0, 5, Position(0, 0)),
    (0, 0, 5, [0, 0]),
    (2, 5, [4, 7], 43),
    (2, 5, Position(4, 7), 43)
])
def test_position_multiplication(x1, y1, multipler, expect):
    pos_1 = Position(x1, y1)
    result = pos_1 * multipler

    if isinstance(expect, (Position, list, tuple)):
        assert result[0] == expect[0] and result[1] == expect[1]
        assert result == expect
    else:
        assert result == expect


@pytest.mark.parametrize("x1, y1, x2, y2, expect", [
    (0, 0, 3, 4, 5),
    (22, 13, 15, 29, 17.4642),
    (1, 5, 24, 31, 34.7131)
])
def test_position_distance(x1, y1, x2, y2, expect):
    pos_1 = Position(x1, y1)
    pos_2 = Position(x2, y2)
    dist = pos_1.distance_to(pos_2)
    assert almost_equal(dist, expect, 10e-4)


def test_position_get_item_exception():
    pos = Position(1, 2)
    with pytest.raises(IndexError):
        val = pos[2]