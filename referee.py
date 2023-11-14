import enum
from piece import PieceTeam


class GameStatus(enum.Enum):
    TIED = 0
    RED_WINS = 1
    BLUE_WINS = 2


class MoveStatus(enum.Enum):
    INVALID = 0
    SUCCESS = 1
    FINAL = 2


class MoveType(enum.Enum):
    HIGH_RANK_PIECE_ATTACK = 1
    GET_IN_CAMP = 2
    RUN_AWAY_FROM_CHASE = 3
    THROW_BOMB_AT_HIGH_RANK = 4
    LOW_RANK_PIECE_TEST_BOMB = 5
    BLOCK_RAILROAD_PATH = 6
    GONGBING_CLEARS_MINE = 7
    LOW_RANK_CHASE_HIGH_RANK = 8
    FALSE_BOMB_THREAT = 9
    DEFEND_FLAG_CAPTURE = 10
    WAIT_OR_NO_PURPOSE_MOVE = 11
    EXPOSE_BOMB = 12
    TEST_MINE = 13
    CAPTURE_FLAG = 14
    DEFEND_MINE = 15
    DEFEND_BOMB = 16
    GET_IN_HEADQUARTER_ZONE = 17
    PUT_PIECE_ON_RAILROAD = 18
    CHASE_OPPONENT = 19
    BOMB_BEHIND_PIECE = 20
    TEST_GONGBING = 21


# {Piece_type: value}
piece_value = {0: 600, 1: 600, 2: 2, 3: 3, 4: 10, 5: 30, 6: 70, 7: 150, 8: 400, 9: 500, 10: 600}


class Referee:
    @staticmethod
    def validate_move(game_board, turn, from_x, from_y, to_x, to_y):
        if from_x > 12 or from_x < 0 or to_x > 12 or to_x < 0 or from_y < 0 or from_y > 4 or to_y < 0 or to_y > 4 or (
                from_x == to_x and from_y == to_y):
            return False

        from_pos = game_board.get_position(from_x, from_y)
        if not from_pos.has_piece() or from_pos.is_headquarter():
            return False

        piece_from_pos = from_pos.get_piece()
        if piece_from_pos.get_team() != turn:
            return False

        if not piece_from_pos.is_moveable():
            return False

        to_pos = game_board.get_position(to_x, to_y)
        piece_to_pos = to_pos.get_piece()
        if piece_to_pos is not None and piece_to_pos.get_team() == turn:
            return False

        if to_pos.has_piece() and to_pos.is_a_camp():
            return False

        if to_pos.is_river() or to_pos.is_bridge():
            return False

        if from_pos.is_railroad():
            if to_pos.is_railroad():
                if Referee.pieces_in_between(game_board, piece_from_pos, from_x, from_y, to_x, to_y):
                    return False
            elif to_pos.is_headquarter():
                if from_y != to_y or abs(from_x - to_x) != 1:
                    return False
            elif to_pos.is_a_camp():
                if abs(from_x - to_x) != 1 and abs(from_y - to_y) != 1:
                    return False
            elif to_pos.is_country_road():
                if from_x == to_x and abs(from_y - to_y) != 1:
                    return False
                elif from_y == to_y and abs(from_x - to_x) != 1:
                    return False
                elif from_x != to_x and from_y != to_y:
                    return False
        elif from_pos.is_country_road():
            if from_x != to_x and abs(from_x - to_x) != 1:
                return False
            elif from_y != to_y and abs(from_y - to_y) != 1:
                return False
            elif from_x != to_x and from_y != to_y:
                return False
        elif from_pos.is_a_camp():
            if abs(from_x - to_x) > 1 or abs(from_y - to_y) > 1:
                return False

        return True

    @staticmethod
    def pieces_in_between(game_board, piece_from_pos, from_x, from_y, to_x, to_y):
        if (from_x != to_x and from_y == to_y and from_y != 0 and from_y != 4 and abs(from_x - to_x) > 2) or (
                from_x != to_x and from_y != to_y):
            if not piece_from_pos.is_gongbing():
                return True
            else:
                return Referee.is_railroad_path_clear(game_board, from_x, from_y, to_x, to_y) == False

        if from_x == to_x:
            step_size = 1 if from_y < to_y else -1
            for y in range(from_y, to_y, step_size):
                if y == from_y:
                    continue

                if game_board.get_position(from_x, y).has_piece():
                    return True

        if from_y == to_y:
            step_size = 1 if from_x < to_x else -1
            for x in range(from_x, to_x, step_size):
                if x == from_x:
                    continue

                if game_board.get_position(x, from_y).has_piece():
                    return True

        return False

    # use bfs on all connected railroad positions starting from (from_x, from_y)
    @staticmethod
    def is_railroad_path_clear(game_board, from_x, from_y, to_x, to_y):
        q = [from_x, from_y]
        visited = set()
        visited.add(game_board.get_position(from_x, from_y).get_id())
        while len(q) > 0:
            current_x = q.pop(0)
            current_y = q.pop(0)
            visited_len = len(visited)
            if current_y != 0 and game_board.get_position(current_x, current_y - 1).is_railroad():
                if to_x == current_x and to_y == current_y - 1:  # found target and no block in between
                    return True

                pos = game_board.get_position(current_x, current_y - 1)
                visited.add(pos.get_id())
                if visited_len < len(visited) and not pos.has_piece():
                    q.extend([current_x, current_y - 1])
                    visited_len = len(visited)

            if current_y != 4 and game_board.get_position(current_x, current_y + 1).is_railroad():
                if to_x == current_x and to_y == current_y + 1:  # found target and no block in between
                    return True

                pos = game_board.get_position(current_x, current_y + 1)
                visited.add(pos.get_id())
                if visited_len < len(visited) and not pos.has_piece():
                    q.extend([current_x, current_y + 1])
                    visited_len = len(visited)

            if current_x != 1 and (
                    game_board.get_position(current_x - 1, current_y).is_railroad() or game_board.get_position(
                current_x - 1, current_y).is_bridge()):
                if to_x == current_x - 1 and to_y == current_y:  # found target and no block in between
                    return True

                pos = game_board.get_position(current_x - 1, current_y)
                visited.add(pos.get_id())
                if visited_len < len(visited) and not pos.has_piece():
                    q.extend([current_x - 1, current_y])
                    visited_len = len(visited)

            if current_x != 11 and (
                    game_board.get_position(current_x + 1, current_y).is_railroad() or game_board.get_position(
                current_x + 1, current_y).is_bridge()):
                if to_x == current_x + 1 and to_y == current_y:  # found target and no block in between
                    return True

                pos = game_board.get_position(current_x + 1, current_y)
                visited.add(pos.get_id())
                if visited_len < len(visited) and not pos.has_piece():
                    q.extend([current_x + 1, current_y])

        return False

    @staticmethod
    def move(game_board, turn, from_x, from_y, to_x, to_y, red_team, blue_team):
        if not Referee.validate_move(game_board, turn, from_x, from_y, to_x, to_y):
            return MoveStatus.INVALID

        from_team = red_team if turn == PieceTeam.RED else blue_team
        to_team = red_team if turn == PieceTeam.BLUE else blue_team

        # remove piece at from
        from_pos = game_board.get_position(from_x, from_y)
        to_pos = game_board.get_position(to_x, to_y)

        from_piece = from_pos.get_piece()
        to_piece = to_pos.get_piece() if to_pos.has_piece() else None
        from_pos.set_is_occupied(False, None)

        # Case 1: To position is empty
        if to_piece is None:
            to_pos.set_is_occupied(True, from_piece)
            if to_pos.is_headquarter():
                from_piece.set_not_moveable()

            return MoveStatus.SUCCESS
        else:
            # Case 2: To position has opponent's piece, compare the rank
            compare_result = 0  # 0-both dead 1-from's team higher 2-to's team higher
            # flag captured. team of this turn wins the game
            if to_piece.is_flag():
                return MoveStatus.FINAL
            elif from_piece.is_gongbing() and to_piece.is_mine():
                from_piece.set_possible_rank(1)
                compare_result = 1
            elif from_piece.is_bomb() or to_piece.is_bomb() or from_piece.get_rank() == to_piece.get_rank():
                compare_result = 0
            elif from_piece.get_rank().value > to_piece.get_rank().value:
                from_piece.set_possible_rank(to_piece.get_rank().value + 1)
                compare_result = 1
            else:
                to_piece.set_possible_rank(from_piece.get_rank().value + 1)
                compare_result = 2

            if compare_result == 0:
                Referee.check_is_siling_and_expose_flag(game_board, from_piece)
                Referee.check_is_siling_and_expose_flag(game_board, to_piece)
                to_pos.set_is_occupied(False, None)
                from_team.remove_alive_piece(from_piece)
                to_team.remove_alive_piece(to_piece)
                from_team.deduct_value(piece_value[from_piece.get_rank().value])
                to_team.deduct_value(piece_value[to_piece.get_rank().value])
                from_piece = None
                to_piece = None
            elif compare_result == 1:
                Referee.check_is_siling_and_expose_flag(game_board, to_piece)
                to_pos.set_is_occupied(True, from_piece)
                to_team.remove_alive_piece(to_piece)
                to_team.deduct_value(piece_value[to_piece.get_rank().value])
                to_piece = None
            else:
                Referee.check_is_siling_and_expose_flag(game_board, from_piece)
                from_team.remove_alive_piece(from_piece)
                from_team.deduct_value(piece_value[from_piece.get_rank().value])
                from_piece = None

        return MoveStatus.SUCCESS

    @staticmethod
    def check_is_siling_and_expose_flag(game_board, piece):
        if piece.is_siling():
            flag_y = game_board.get_team_flag_y_location(piece.get_team())
            flag_x = 0 if piece.get_team() == PieceTeam.BLUE else 12
            # set team's flag exposed
            game_board.get_position(flag_x, flag_y).get_piece().set_is_exposed()
