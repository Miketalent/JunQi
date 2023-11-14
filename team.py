class Team:
    def __init__(self, team, alive_pieces):
        self._team = team
        self._alive_pieces = alive_pieces
        self._possible_dead_pieces = []
        self._game_value = 6235  # based on total value of alive pieces

    def get_alive_pieces(self):
        return self._alive_pieces

    def remove_alive_piece(self, piece):
        self._alive_pieces.remove(piece)

    # piece is pieceType enum value
    def add_possible_dead_piece(self, piece):
        self._possible_dead_pieces.append(piece)
        self._possible_dead_pieces.sort(reverse=True)

    def get_possible_dead_pieces(self):
        return self._possible_dead_pieces

    def get_game_value(self):
        return self._game_value

    def deduct_value(self, value):
        self._game_value = self._game_value - value
