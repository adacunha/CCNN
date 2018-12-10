import tensorflow as tf
import numpy as np

import AlphaCheckers
import Checkers

board = Checkers.Board()
alpha_player = AlphaCheckers.Player()

alpha_move = alpha_player.play_turn(board, board.get_black_piece())

print(alpha_move)
