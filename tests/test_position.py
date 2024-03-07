from Position import Position


def test_position_addition():
    pos_1 = Position(1, 4)
    pos_2 = Position(2, 6)
    pos_3 = pos_1 + pos_2
    assert pos_3.x == 3 and pos_3.y == 10


def test_position_distance():
    pos_1 = Position(2, 5)
    pos_2 = Position(6, 8)
    dist = pos_1.distance_to(pos_2)
    assert dist == 5
