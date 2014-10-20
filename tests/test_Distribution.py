import unittest

from Distribution import Distribution

class DistributionTestCase(unittest.TestCase):
	def test_createDistribution(self):
		rate, dist = 3, {1: 0.5, 2: 0.5}
		distribution = Distribution(rate, dist)
		self.assertEqual(distribution.rate, rate)
		self.assertEqual(distribution.packet(1), 0.5)
		self.assertEqual(distribution.packet(2), 0.5)


if __name__ == '__main__':
	unittest.main()
