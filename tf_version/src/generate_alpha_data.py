
import TTT

board = TTT.Board(3);

data_file = open("random_games_train_test.dat", "a")
board.log_to(data_file)

training_size = 100

start_player = 1
count = 0;
while(True):
	print("Gathering data on game: " + str(count))
	count += 1
	board.refresh()
	current_player = start_player
	start_player *= -1
	while(not board.has_won() and not board.drawn()):
		best_play = board.negamax(current_player)
		board.random_move(current_player);
		current_player *= -1
	
