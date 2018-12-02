import tensorflow as tf
import numpy as np
from tensorflow.keras import layers
import matplotlib.pyplot as plt

import TTT

board = TTT.Board(3);

board.place_piece(1, 1, 1);
board.place_piece(1, 0, 1);
board.place_piece(1, 2, 1);

if(1 != board.has_won()):
	print("BOARD WIN ERROR 1")

board.remove_piece(1, 1);
if(1 == board.has_won()):
	print("BOARD REMOVE WIN ERRROR")

board.place_piece(2, 0, -1);
board.place_piece(1, 1, -1);
board.place_piece(0, 2, -1);
if(-1 != board.has_won()):
	print("BOARD REPLACE ERROR");

board.remove_piece(0, 2);
board.place_piece(0, 0, -1);
board.place_piece(2, 2, -1);

if(-1 != board.has_won()):
	print("WTF")
