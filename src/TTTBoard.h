#ifndef __TTTBOARD_H_
#define __TTTBOARD_H_

#include "Board.h"

#define X 1
#define O -1

#define size 3

class TTTBoard : public Board {
	public:
		TTTBoard() : Board(size, size) {
		}
		bool place_X(int row_i, int col_i){
			return this->place_piece(X, row_i, col_i);
		}	
		bool place_O(int row_i, int col_i){
			return this->place_piece(O, row_i, col_i);
		}
		bool O_victor(){
			return consecutive_count(O, 3);		
		}			
		bool X_victor(){
			return consecutive_count(X, 3);
		}
		bool is_drawn(){
			if(this->O_victor() || this->X_victor()) return false;
			return this->get_piece_count() == size*size;
		}
	private:
		bool consecutive_count(Piece p, int count){
			for(int i = 0; i < size; ++i){
				Piece row_match = this->get_piece(i, 0);
				Piece col_match = this->get_piece(0, i);
				
				bool row_valid = row_match == p;
				bool col_valid = col_match == p;
				for(int j=1; j < size; ++j){
					if(this->get_piece(i, j) != row_match) row_valid = false;
					if(this->get_piece(j, i) != col_match) col_valid = false;
				}
				if(row_valid || col_valid) return true;
			}
			Piece diag_match_left = this->get_piece(0, 0);
			Piece diag_match_right = this->get_piece(size-1, size-1);
			bool diag_valid_left = diag_match_left == p;
			bool diag_valid_right = diag_match_right == p;
			for(int i=1; i<size; ++i){
				if(this->get_piece(i, i) != diag_match_left) diag_valid_left = false;
				if(this->get_piece(i, size-1-i) != diag_match_right) diag_valid_right = false;
			}
			return diag_valid_left || diag_valid_right;
		}
};

#endif
