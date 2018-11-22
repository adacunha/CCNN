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
		std::vector<double> feed_forward(const std::vector<double>& input);

	public:	

		NN(const std::vector<int>& layer_sizes);

		double train(const std::vector<const std::vector<double>>& data);

		void print_weights();
};

#endif
