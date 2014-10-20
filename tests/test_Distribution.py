import unittest

from Distribution import Distribution

class InvalidDistributionTestCase(unittest.TestCase):
	def test_createInvalidDistribution(self):
		with self.assertRaises(ValueError):
			rate, dist = 3, {1: 0.5, 2: 0.25}
			Distribution(rate, dist)

class DistributionTestCase(unittest.TestCase):
	def setUp(self):
		self.rate, self.dist = 3, {1: 0.5, 2: 0.5}
		self.distribution = Distribution(self.rate, self.dist)

	def test_createDistribution(self):
		self.assertEqual(self.distribution.rate, self.rate)
		self.assertEqual(self.distribution.probability(1), self.dist[1])
		self.assertEqual(self.distribution.probability(2), self.dist[2])

	def test_getPacktes(self):
		self.assertEqual(self.distribution.packets, [1, 2])

if __name__ == '__main__':
	unittest.main()
