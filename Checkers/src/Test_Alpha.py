import tensorflow as tf
import numpy as np

import AlphaCheckers
import Checkers

board = Checkers.Board()
alpha_player = AlphaCheckers.Player(board.get_black_piece())

alpha_player.evaluate_turn_policy(board)
alpha_player.evaluate_turn_value(board)

