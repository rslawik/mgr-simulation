import unittest

from Distribution import Distribution

class InvalidDistributionTestCase(unittest.TestCase):
	def test_createDistribution(self):
		with self.assertRaises(ValueError):
			rate, dist = 3, {1: 0.5, 2: 0.25}
			Distribution(rate, dist)

class DistributionTestCase(unittest.TestCase):
	def setUp(self):
		self.rate, self.dist = 3, {1: 0.5, 2: 0.25, 1.5: 0.25}
		self.distribution = Distribution(self.rate, self.dist)

	def test_createDistribution(self):
		self.assertEqual(self.distribution.rate, self.rate)
		self.assertEqual(self.distribution.probability(1), self.dist[1])
		self.assertEqual(self.distribution.probability(2), self.dist[2])

	def test_getPacktes(self):
		self.assertEqual(self.distribution.packets, [1, 1.5, 2])

class DistributionFromFileTestCase(unittest.TestCase):
	def test_createDistributionNoFile(self):
		with self.assertRaises(FileNotFoundError):
			distribution = Distribution.fromFile('tests/example/test_Distribution.inXXX')

	def test_createDistribution(self):
		distribution = Distribution.fromFile('tests/example/distribution.in')
		self.assertEqual(distribution.packets, [3, 5, 7])
		self.assertEqual(distribution.rate, 5)
		self.assertEqual(distribution.probability(3.0), 0.33)
		self.assertEqual(distribution.probability(5.0), 0.17)
		self.assertEqual(distribution.probability(7.0), 0.5)

	def test_createDistributionWithoutInfo(self):
		distribution = Distribution.fromFile('tests/example/packets.in')
		self.assertEqual(distribution.packets, [3, 5, 7])
		self.assertEqual(distribution.rate, None)
		self.assertEqual(distribution.probability(5.0), None)

if __name__ == '__main__':
	unittest.main()
