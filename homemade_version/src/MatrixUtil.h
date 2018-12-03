#ifndef __MATRIXUTIL_H_
#define __MATRIXUTIL_H_

#include <vector>
#include <iostream>

std::vector<std::vector<double>> matrix_mult(const std::vector<std::vector<double>>& A, const std::vector<std::vector<double>>& B);

std::vector<std::vector<double>> matrix_transpose(const std::vector<std::vector<double>>& A);

void print_matrix(const std::vector<std::vector<double>>& A);

void matrix_size(const std::vector<std::vector<double>>& A);

#endif
