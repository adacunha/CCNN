
class Board:
	
	def __init__(self):
		self.side_length = 8
		self.refresh()

	def refresh(self):
		self.occupied_squares = {}
		self.unoccupied_squares = set();

		for i in range(1, 33):
			self.unoccupied_squares.add(i)
		
		for i in range(1, 13):
			self.place_own_pawn(1, i)

		for i in range(21, 33):
			self.place_own_pawn(-1, i)

	def place_opponent_pawn(self, player, coord):
		piece = -1 if player == 1 else 1
		self.place_piece(coord, piece)	

	def place_own_pawn(self, player, coord):
		piece = 1 if player == 1 else -1
		self.place_piece(coord, piece)

	def place_opponent_king(self, player, coord):
		piece = -2 if player == 1 else 2
		self.place_piece(coord, piece)

	def place_own_king(self, player, coord):
		piece = 2 if player == 1 else -2
		self.place_piece(coord, piece)

	def place_piece(self, coord, piece):
		self.unoccupied_squares.remove(coord)
		self.occupied_squares[coord] = piece
	
	def remove_piece(self, coord):
		self.occupied_squares.remove(coord)
		self.unoccupied_squares.add(coord)

	def get_piece(self, coord):
		if coord in self.occupied_squares:
			return self.occupied_squares[coord];
		return 0
		
	def show(self):
		for i in range(0, 32):
			if i != 0 and not i%4 and int(i/4)&1:
				print()
			else:
				print(" ", end='')
			if not i%4 and not int(i/4)&1:
				print()
			print(self.get_piece(i+1), end='')
		print(" ", end='')
	
	def get_nn_input(self):
		return [self.get_piece(i) for i in range(1, 33)]
