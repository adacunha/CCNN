import Checkers
import re

raw_data_path = "../data/games.txt"
parsed_data_path = "../data/parsed_games.txt"

board = Checkers.Board()

def get_turn_data(board, current_player, turn):
	data = []
	capturing = False
	jumps = turn.split('-')
	if len(jumps) == 1:
		capturing = True
		jumps = turn.split('x')

	for i in range(1, len(jumps)):
		start = int(jumps[i-1])
		end = int(jumps[i])
		data.append((board.get_nn_input(current_player), board.get_nn_output((start, end))))
		if capturing:
			board.capture((start, end))
		else:
			board.move_piece((start, end))
	return data

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
		turn_data.extend(move_data)
		current_player = black_piece if current_player == white_piece else white_piece		

	return turn_data

train_data = []

with open(raw_data_path, 'r') as data_file:
	game_str = ""
	for line in data_file:
		if line[0] != '[':
			line = line.strip()
			if len(line) == 0:
				orig_game_str = game_str
				game_str = re.sub(r'\{[^\}]*\}', '', game_str)
				#try:
				train_data.extend(get_game_data(board, game_str))
				#except:
				#	print("EXCEPTION ON PARSE: ")
				#	board.show()
				#	break
				board.refresh()
				game_str = ""
			else:
				game_str = game_str + " " + line

with open(parsed_data_path, 'w') as output_file:
	for data_point in train_data:
		x = data_point[0]
		y = data_point[1]	
		for val in x:
			output_file.write(str(val) + " ")
		for val in y:
			output_file.write(str(val) + " ")
		output_file.write("\n")
