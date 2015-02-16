#include <iostream>
#include <random>
#include <chrono>
using namespace std;

int main() {
	ios_base::sync_with_stdio(false);

	const int n = 1e6;

	unsigned seed = chrono::system_clock::now().time_since_epoch().count();
	// minstd_rand0 generator(seed);
	mt19937 generator(seed);
  	exponential_distribution<double> distribution(0.05);

  	double time = 0.0;
	for (int i = 0; i < n; i++) {
		cout << time << " 47.0\n";
		double interval = distribution(generator);
		time += interval;
	}

	return 0;
}
