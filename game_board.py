from position import *
from util import get_name
from piece import *


class GameBoard:
    def __init__(self, board_map, red_config, blue_config):
        self._board = [[0 for _ in range(5)] for _ in range(13)]
        self._red_pieces_loaded = []
        self._blue_pieces_loaded = []
        self._blue_team_flag_y = 0
        self._red_team_flag_y = 0
        self._pos_by_id = [None]
        self._construct_board(board_map)
        self._load_team_pieces(red_config, blue_config)

    # load map.config the types of each square in the game board
    def _construct_board(self, board_map):
        map_config = open(board_map, 'r').readlines()
        id_count = 1
        for x in range(13):
            line = map_config[x].split()
            index = 0
            for y in range(5):
                pos_type = int(line[index])
                a_pos = Position(id_count, pos_type, False)
                self._board[x][y] = a_pos
                self._pos_by_id.append(a_pos)
                id_count = id_count + 1
                index = index + 1

    # fill board with team red and blue's piece arrangement
    def _load_team_pieces(self, red_config, blue_config):
        red_config = open(red_config, 'r').readlines()
        blue_config = open(blue_config, 'r').readlines()

        # fill in blue team first: right to left, bottom up
        line_index = 0
        for x in range(5, -1, -1):
            index = 0
            line = blue_config[line_index].split()
            print(line)
            line_index = line_index + 1
            for y in range(4, -1, -1):
                pos = self.get_position(x, y)
                if pos.is_a_camp():
                    continue

                piece_type = int(line[index])
                piece = Piece(get_name(piece_type), piece_type, PieceTeam.BLUE, get_name(piece_type))
                self._blue_pieces_loaded.append(piece)
                pos.set_is_occupied(True, piece)
                if piece.is_flag():
                    self._blue_team_flag_y = y
                index = index + 1

        for x in range(7, 13):
            line = red_config[x - 7].split()
            index = 0
            for y in range(5):
                pos = self.get_position(x, y)
                if pos.is_a_camp():
                    continue

                piece_type = int(line[index])
                index = index + 1
                piece = Piece(get_name(piece_type), piece_type, PieceTeam.RED, get_name(piece_type))
                self._red_pieces_loaded.append(piece)
                pos.set_is_occupied(True, piece)
                if piece.is_flag():
                    self._red_team_flag_y = y

    def get_position(self, x, y):
        return self._board[x][y]

    def get_position_by_id(self, id):
        return self._pos_by_id[id]

    def get_pieces_loaded(self, team):
        if team == PieceTeam.RED:
            return self._red_pieces_loaded

        return self._blue_pieces_loaded

    def get_team_flag_y_location(self, team):
        return self._red_team_flag_y if team == PieceTeam.RED else self._blue_team_flag_y
