import Checkers
import tensorflow as tf
import numpy as np


data_path = "../data/games.txt"

board = Checkers.Board()

def get_turn_coords(turn):
	squares = turn.split('-')
	if len(squares) == 1:
		squares = turn.split('x')
	if len(squares) < 2:
		print("TURN PARSING FUCKED UP ON: " + turn)
	from_square = int(squares[0])
	to_square = int(squares[len(squares)-1])
	return (from_square, to_square)

def get_turn_data(board, current_player, turn):
	turn_coords = get_turn_coords(turn)
	return (board.get_nn_input(current_player), turn_coords)	

def make_move(board, turn):
	jumps = turn.split('x')
	if len(jumps) == 1:
		board.move_piece(get_turn_coords(turn))
		return
	for i in range(1, len(jumps)):
		last = int(jumps[i-1])
		next = int(jumps[i])	
		board.capture((last, next))

def get_game_data(board, game_str):

	turns = game_str.split()

	black_piece = board.get_black_piece()
	white_piece = board.get_white_piece()
	current_player = black_piece

	turn_data = []

	for i, turn in enumerate(turns[:-1]):
		if not i%3:
			continue
		move_data = get_turn_data(board, current_player, turn)
		turn_data.append(move_data)
		make_move(board, turn)
		current_player = black_piece if current_player == white_piece else white_piece		

	return turn_data

train_data = []

with open(data_path, 'r') as data_file:
	game_str = ""
	for line in data_file:
		if line[0] != '[':
			line = line.strip()
			if len(line) == 0:
				train_data.extend(get_game_data(board, game_str))
				board.refresh()
				game_str = ""
				break
			else:
				game_str = game_str + " " + line

print(train_data)
