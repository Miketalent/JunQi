import enum


class PositionType(enum.Enum):
    BRIDGE = 0
    RAILROAD = 1
    COUNTRYROAD = 2
    CAMP = 3
    HEADQUARTER = 4
    RIVER = 5


class Position:
    def __init__(self, pos_id, pos_type, is_occupied):
        self._type = PositionType(pos_type)
        self._is_occupied = is_occupied
        self._piece = None
        self._id = pos_id

    def get_id(self):
        return self._id

    def set_is_occupied(self, occupied, piece):
        self._is_occupied = occupied
        self._piece = piece

    def has_piece(self):
        return self._is_occupied

    def get_piece(self):
        return self._piece

    def is_a_camp(self):
        return self._type == PositionType.CAMP

    def is_river(self):
        return self._type == PositionType.RIVER

    def is_bridge(self):
        return self._type == PositionType.BRIDGE

    def is_headquarter(self):
        return self._type == PositionType.HEADQUARTER

    def is_railroad(self):
        return self._type == PositionType.RAILROAD

    def is_country_road(self):
        return self._type == PositionType.COUNTRYROAD
