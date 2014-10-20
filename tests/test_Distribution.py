import unittest

from Distribution import Distribution

class InvalidDistributionTestCase(unittest.TestCase):
	def test_createInvalidDistribution(self):
		with self.assertRaises(ValueError):
			rate, dist = 3, {1: 0.5, 2: 0.25}
			Distribution(rate, dist)

class DistributionTestCase(unittest.TestCase):
	def test_createDistribution(self):
		rate, dist = 3, {1: 0.5, 2: 0.5}
		distribution = Distribution(rate, dist)
		self.assertEqual(distribution.rate, rate)
		self.assertEqual(distribution.packet(1), 0.5)
		self.assertEqual(distribution.packet(2), 0.5)

	def test_getPacktes(self):
		pass

if __name__ == '__main__':
	unittest.main()
