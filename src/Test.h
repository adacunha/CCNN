#include "Board.h"
#include "TTTBoard.h"
#include "NN.h"

#include <iostream>

#define assert_equals(x, y, m) if((x) != (y)) std::cout << "FAILED TEST: " << (m) << std::endl

void test_TTTBoard();

void test_Board();

void test_NN();

void test_build(){
	test_Board();
	test_TTTBoard();
	test_NN();
}

int main(){
	std::cout << "Testing Build..." << std::endl << std::endl;
	test_build();
	std::cout << "Tests complete" << std::endl;
	return 0;
}