#include "MatrixUtil.h"

std::vector<std::vector<double>> matrix_mult(std::vector<std::vector<double>>& A, std::vector<std::vector<double>>& B){
	if(A.size() && A[0].size() != B.size()){
		std::cout << "Matrix multiplication dimension error!" << std::endl;
		return {{}};
	}
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
