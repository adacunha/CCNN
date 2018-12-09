import Checkers
import re

raw_data_path = "../data/games.txt"
parsed_data_path = "../data/parsed_games.txt"

board = Checkers.Board()

def get_turn_data(board, current_player, turn, winner):
	data = []
	capturing = False
	jumps = turn.split('-')
	if len(jumps) == 1:
		capturing = True
		jumps = turn.split('x')

	for i in range(1, len(jumps)):
		start = int(jumps[i-1])
		end = int(jumps[i])
		data.append((board.get_nn_input(current_player), board.get_nn_output((start, end)), winner))
		if capturing:
			board.capture((start, end))
		else:
			board.move_piece((start, end))
	return data

def get_game_data(board, game_str, winner):

	turns = game_str.split()

	black_piece = board.get_black_piece()
	white_piece = board.get_white_piece()
	current_player = black_piece

	turn_data = []

	winner_hot = [0 for i in range(0, 3)]
	if not winner:
		winner_hot[0] = 1
	elif winner == 1:
		winner_hot[1] = 1
	else:	
		assert(winner == -1)
		winner_hot[2] = 1

	for i, turn in enumerate(turns[:-1]):
		if not i%3:
			continue
		move_data = get_turn_data(board, current_player, turn, winner_hot)
		turn_data.extend(move_data)
		current_player = black_piece if current_player == white_piece else white_piece		

	return turn_data

train_data = []

with open(raw_data_path, 'r') as data_file:
	game_str = ""
	winner = 0
	for line in data_file:
		if line[0] != '[':
			line = line.strip()
			if len(line) == 0:
				orig_game_str = game_str
				game_str = re.sub(r'\{[^\}]*\}', '', game_str)
				#try:
				train_data.extend(get_game_data(board, game_str, winner))
				#except:
				#	print("EXCEPTION ON PARSE: ")
				#	board.show()
				#	break
				board.refresh()
				winner = 0
				game_str = ""
			else:
				game_str = game_str + " " + line
		else:
			line = line.strip()
			if len(line) and line[0] == '[' and line[1] == 'R' and line[2] == 'e':
				winner_str = line.split("\"")[1]
				if len(winner_str.split("/")) > 1:
					winner = 0
				else:
					winner = 1 if int(winner_str.split("-")[0]) == 1 else -1

with open(parsed_data_path, 'w') as output_file:
	for data_point in train_data:
		x = data_point[0]
		y = data_point[1]	
		winner = data_point[2]
		for val in x:
			output_file.write(str(val) + " ")
		for val in y:
			output_file.write(str(val) + " ")
		for val in winner:
			output_file.write(str(val) + " ")
		output_file.write("\n")
