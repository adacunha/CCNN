#ifndef __BOARD_H_
#define __BOARD_H_

#include <vector>
#include <iostream>

// Pieces as integers for now
#define EMPTY_PIECE 0
typedef int Piece;

class Board {

	int width;
	int height;
	std::vector<std::vector<Piece>> grid;

	public:

		Board(int width, int height);

		// Individual piece manipulators
		Piece get_piece(int row_i, int col_i);
		bool remove_piece(int row_i, int col_i);
		bool place_piece(Piece p, int row_i, int col_i);

		// Clear all board pieces
		void clear();

		// Getters + Setters
		int get_piece_count();
		int get_width();
		int get_height();
		void print();

	private:
		int piece_count;

		// Check validity of coordinate
		bool valid_grid(int row_i, int col_i);

		// Check is coordinate contains piece
		bool is_index_occupied(int row_i, int col_i);
};

#endif
