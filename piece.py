import enum


class PieceTeam(enum.Enum):
    RED = 0
    BLUE = 1


class PieceType(enum.Enum):
    EMPTY = -1
    ZHADAN = 0
    GONGBING = 1
    PAIZHANG = 2
    LIANZHANG = 3
    YINGZHANG = 4
    TUANZHANG = 5
    LVZHANG = 6
    SHIZHANG = 7
    JUNZHANG = 8
    SILING = 9
    DILEI = 10
    JUNQI = 99


class Piece:
    def __init__(self, name, rank, team, display_name):
        self._name = name
        self._rank = PieceType(rank)
        self._can_move = self._rank != PieceType.DILEI and self._rank != PieceType.JUNQI
        self._possible_rank = -1
        self._team = PieceTeam(team)
        self._display_name = display_name
        self._is_exposed = False

    def set_is_exposed(self):
        self._is_exposed = True

    def get_is_exposed(self):
        return self._is_exposed

    def set_possible_rank(self, possible_rank):
        self._possible_rank = possible_rank

    def get_possible_rank(self):
        return self._possible_rank

    def get_team(self):
        return self._team

    def set_not_moveable(self):
        self._can_move = False

    def get_name(self):
        return self._name

    def is_moveable(self):
        return self._can_move

    def set_display_name(self, name):
        self._display_name = name

    def get_display_name(self):
        return '*' if not self.get_is_exposed() else self._display_name

    def is_gongbing(self):
        return self._rank == PieceType.GONGBING

    def is_flag(self):
        return self._rank == PieceType.JUNQI

    def is_mine(self):
        return self._rank == PieceType.DILEI

    def is_bomb(self):
        return self._rank == PieceType.ZHADAN

    def is_siling(self):
        return self._rank == PieceType.SILING

    def get_rank(self):
        return self._rank
