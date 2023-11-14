from game_board import *
from util import *
from referee import *
from team import Team
import csv

game_board = GameBoard('map.config', 'red.config', 'blue.config')
file_header = ['move']
for i in range(1, 66):
    file_header.append('pos_id_'+str(i))

file_header.extend(['from_x', 'from_y', 'to_x', 'to_y', 'move_turn', 'move_type', 'move_status', 'red_game_value', 'blue_game_value'])
result_file = "./results/game_5.csv"

team_red = Team(PieceTeam.RED, game_board.get_pieces_loaded(PieceTeam.RED))
team_blue = Team(PieceTeam.BLUE, game_board.get_pieces_loaded(PieceTeam.BLUE))

move_step = 1
next_turn = PieceTeam.BLUE

with open(result_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(file_header)

    # start game
    while True:
        move_status = MoveStatus.INVALID

        # each team's turn to make a move
        while True:
            if next_turn == PieceTeam.RED:
                draw_game_board_red_side(game_board)
            else:
                draw_game_board_blue_side(game_board)

            while True:
                move_input = input(
                    "Make a move. Enter the from and to X and Y value separated by space. Like: 10 2 11 2\n").split()
                if len(move_input) == 4:
                    break

            move_status = Referee.move(game_board, next_turn, int(move_input[0]), int(move_input[1]), int(move_input[2]), int(move_input[3]), team_red, team_blue)

            if move_status != MoveStatus.INVALID:
                print("Successful move!")
                break
            else:
                print("Invalid move!\n")

        move_type = input("Pick the number from following that best describes the type of your move:\n"
                          "1:high rank attack\n"
                          "2:get in camp\n"
                          "3:run away from chase\n"
                          "4:throw bomb at high rank\n"
                          "5:test bomb\n"
                          "6:block railroad path\n"
                          "7:gongbing clears mine\n"
                          "8:low rank bluff\n"
                          "9:false bomb threat\n"
                          "10:defend flag capture\n"
                          "11:wait or no purpose move\n"
                          "12:expose bomb\n"
                          "13:test mine\n"
                          "14:capture flag\n"
                          "15.defend mine\n"
                          "16.defend bomb\n"
                          "17.get into headquarter zone\n"
                          "18.Put piece on railroad\n"
                          "19.Chase opponent\n"
                          "20.Bomb behind piece\n"
                          "21.test gongbing\n")

        # record game board and status after each move
        data = [move_step]
        for i in range(1, 66):
            pos = game_board.get_position_by_id(i)
            rank = pos.get_piece().get_rank().value if pos.has_piece() else -1
            data.append(rank)

        data.extend([int(move_input[0]), int(move_input[1]), int(move_input[2]), int(move_input[3]), next_turn.value, int(move_type), move_status.value, team_red.get_game_value(), team_blue.get_game_value()])
        print(data)
        writer.writerow(data)
        f.flush()

        if move_status == MoveStatus.FINAL:
            print("Game over!\n")
            win_team = "Red Team Wins!" if next_turn == PieceTeam.RED else "Blue Team Wins"
            print(win_team)
            break

        move_step = move_step + 1
        next_turn = PieceTeam.RED if next_turn == PieceTeam.BLUE else PieceTeam.BLUE

