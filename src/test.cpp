#include "Board.h"
#include "TTTBoard.h"

#include <iostream>

#define assert_equals(x, y, m) if((x) != (y)) std::cout << "FAILED TEST: " << (m) << std::endl

void test_TTTBoard(){

	bool t = 1;
	TTTBoard b;

	assert_equals(b.O_victor(), 0, "initial win condition");
	assert_equals(b.X_victor(), 0, "initial win condition");

	assert_equals(b.place_O(0, 0), 1, "initial place condition");
	assert_equals(b.place_O(1, 1), 1, "initial place condition");
	assert_equals(b.place_O(2, 2), 1, "initial place_condition");

	assert_equals(b.O_victor(), 1, "left diag win condition");
	assert_equals(b.X_victor(), 0, "left diag win condition FALSE");
	
	assert_equals(b.place_O(1, 1), 0, "invalid place condition");
	assert_equals(b.O_victor(), 1, "invalid place invariant");
	assert_equals(b.X_victor(), 0, "invalid place invariant");

	assert_equals(b.remove_piece(1, 1), 1, "remove piece");
	assert_equals(b.remove_piece(1, 1), 0, "remove missing piece");
	assert_equals(b.O_victor(), 0, "victor voided condition");
	assert_equals(b.X_victor(), 0, "victor voided condition");

	assert_equals(b.place_X(1, 1), 1, "place condition");
	assert_equals(b.O_victor(), 0, "place victor condition");
	assert_equals(b.X_victor(), 0, "place victor condition");

	assert_equals(b.remove_piece(1, 1), 1, "remove piece condition 1");
	assert_equals(b.remove_piece(2, 2), 1, "remove piece condition 2");
	assert_equals(b.remove_piece(0, 0), 1, "remove piece condition 3");

	for(int i=0; i<3; ++i){
		for(int j=0; j<3; ++j){
			assert_equals(b.place_X(i, j), 1, "place piece bulk");
		}
	}
	assert_equals(b.is_drawn(), false, "drawn when won");
	
	b.clear();
	assert_equals(b.get_piece_count(), 0, "clear test");

	b.place_O(0, 0);
	b.place_O(1, 0);
	b.place_O(0, 2);
	b.place_X(0, 1);
	b.place_X(2, 0);
	b.place_O(2, 1);
	b.place_X(1, 2);
	b.place_X(2, 2);
	b.place_O(1, 1);
	b.place_O(2, 1);

	assert_equals(b.X_victor(), false, "x draw test");
	assert_equals(b.O_victor(), false, "o draw test");
	assert_equals(b.is_drawn(), true, "drawn test");
	assert_equals(b.get_piece_count(), 9, "bulk piece count");
}

void test_Board(){
	Board b(10, 5);
	assert_equals(b.get_piece_count(), 0, "board piece count");
	assert_equals(b.get_width(), 10, "board width");
	assert_equals(b.get_height(), 5, "board height");
	assert_equals(b.place_piece(1, 1, 1), 1, "board place");
	assert_equals(b.get_piece_count(), 1, "board count");
	assert_equals(b.place_piece(1, 1, 1), 0, "board place");
	assert_equals(b.get_piece_count(), 1, "board count");
	assert_equals(b.remove_piece(1, 1), 1, "board remove");
	assert_equals(b.remove_piece(1, 1), 0, "board remove2");
	assert_equals(b.get_piece_count(), 0, "board count");
}

void test_build(){
	test_Board();
	test_TTTBoard();
}

int main(){
	std::cout << "Testing Build..." << std::endl << std::endl;
	test_build();
	std::cout << "Tests complete" << std::endl;
	return 0;
}
