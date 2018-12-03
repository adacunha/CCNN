#include "MatrixUtil.h"

std::vector<std::vector<double>> matrix_mult(const std::vector<std::vector<double>>& A, const std::vector<std::vector<double>>& B){
	if(A.size() && A[0].size() != B.size()) throw "MATRIX MULTIPLICATION DIMENSION ERROR!\n";
	std::vector<std::vector<double>> result(A.size(), std::vector<double>(B[0].size(), 0));
	for(int i=0; i<A.size(); ++i){
		for(int j=0; j<B[0].size(); ++j){
			for(int k=0; k<A[0].size(); ++k){
				result[i][j] += A[i][k] * B[k][j];
			}
		}
	}
	return result;
}

std::vector<std::vector<double>> matrix_transpose(const std::vector<std::vector<double>>& A){
	std::vector<std::vector<double>> result(A[0].size(), std::vector<double>(A.size()));
	for(int i=0; i<A.size(); ++i){
		for(int j=0; j<A[0].size(); ++j){
			result[j][i] = A[i][j];
		}
	}
	return result;
}

void print_matrix(const std::vector<std::vector<double>>& A){
	std::cout << std::endl;
	for(int i=0; i<A.size(); ++i){
		for(int j=0; j<A[0].size(); ++j){
			std::cout << A[i][j] << " ";		
		}
		std::cout << std::endl;
	}
	std::cout << std::endl;
}

void matrix_size(const std::vector<std::vector<double>>& A){
	std::cout << "(" << A.size() << "," << A[0].size() << ")" << std::endl;

}
