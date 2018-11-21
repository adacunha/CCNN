#ifndef __NN_H_
#define __NN_H_

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include <vector>
#include <iostream>

class NN {

	private:

		int num_layers;
		std::vector<std::vector<std::vector<double>>> weights;
		std::vector<std::vector<double>> layers;

	public:	

		NN(std::vector<int> layer_sizes);

		void print_weights();

		std::vector<double> feed_forward(std::vector<double> input);
};

#endif
