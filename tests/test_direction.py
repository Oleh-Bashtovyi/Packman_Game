from Direction import Direction


def test_direction_opposite():
    assert Direction.NONE.opposite() == Direction.NONE
    assert Direction.DOWN.opposite() == Direction.UP
    assert Direction.UP.opposite() == Direction.DOWN
    assert Direction.LEFT.opposite() == Direction.RIGHT
    assert Direction.RIGHT.opposite() == Direction.LEFT


def test_shift():
    assert Direction.NONE.to_shift() == (0, 0)
    assert Direction.UP.to_shift() == (0, -1)
    assert Direction.DOWN.to_shift() == (0, 1)
    assert Direction.LEFT.to_shift() == (-1, 0)
    assert Direction.RIGHT.to_shift() == (1, 0)
