#!/usr/bin/python
# -*- coding: utf-8 -*-
from piece import PieceType
from colorama import Fore

def get_name(type):
    piece_type = PieceType(type)
    if piece_type == PieceType.GONGBING:
        return '工'
    elif piece_type == PieceType.PAIZHANG:
        return '排'
    elif piece_type == PieceType.LIANZHANG:
        return '连'
    elif piece_type == PieceType.YINGZHANG:
        return '营'
    elif piece_type == PieceType.TUANZHANG:
        return '团'
    elif piece_type == PieceType.LVZHANG:
        return '旅'
    elif piece_type == PieceType.SHIZHANG:
        return '师'
    elif piece_type == PieceType.JUNZHANG:
        return '军'
    elif piece_type == PieceType.SILING:
        return '司'
    elif piece_type == PieceType.DILEI:
        return '雷'
    elif piece_type == PieceType.ZHADAN:
        return '弹'
    elif piece_type == PieceType.JUNQI:
        return '旗'

def draw_game_board_red_side(board):
    for x in range(13):
        print('\n')
        for y in range(5):
            pos = board.get_position(x, y)
            piece = pos.get_piece()
            name = '_' if not pos.has_piece() else (piece.get_name() if piece.get_team().value == 0 else piece.get_display_name())
            if pos.is_railroad():
                print(Fore.WHITE + name, str(x) + str(y), '    ', end = '')
            elif pos.is_country_road():
                print(Fore.GREEN + name, str(x) + str(y), '    ', end = '')
            elif pos.is_bridge():
                print(Fore.CYAN + '桥', str(x) + str(y), '    ', end = '')
            elif pos.is_a_camp():
                print(Fore.CYAN + name, str(x) + str(y), '    ', end = '')
            elif pos.is_headquarter():
                print(Fore.MAGENTA + name, str(x) + str(y), '    ', end = '')
            elif pos.is_river():
                print(Fore.CYAN + '河', str(x) + str(y), '    ', end = '')

    print('\n')

def draw_game_board_blue_side(board):
    for x in range(12, -1, -1):
        print('\n')
        for y in range(4, -1, -1):
            pos = board.get_position(x, y)
            piece = pos.get_piece()
            name = '_' if not pos.has_piece() else (piece.get_name() if piece.get_team().value == 1 else piece.get_display_name())
            if pos.is_railroad():
                print(Fore.WHITE + name, str(x) + str(y), '    ', end = '')
            elif pos.is_country_road():
                print(Fore.GREEN + name, str(x) + str(y), '    ', end = '')
            elif pos.is_bridge():
                print(Fore.CYAN + '桥', str(x) + str(y), '    ', end = '')
            elif pos.is_a_camp():
                print(Fore.CYAN + name, str(x) + str(y), '    ', end = '')
            elif pos.is_headquarter():
                print(Fore.MAGENTA + name, str(x) + str(y), '    ', end = '')
            elif pos.is_river():
                print(Fore.CYAN + '河', str(x) + str(y), '    ', end = '')

    print('\n')
