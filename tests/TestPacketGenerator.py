import unittest

import PacketGenerator
from Distribution import Distribution

class PacketGeneratorTestCase(unittest.TestCase):
	def test_experiment1iteration(self):
		distribution = Distribution(None, {3: None, 5: None})
		expected = [(0, 3), (0, 5), (8, 3), (8, 5), (16, 3), (16, 5)]
		generator = PacketGenerator.experiment1(6, distribution)
		for ie, eic in zip(generator, expected):
			self.assertEqual(ie, eic)

	def test_experiment1length(self):
		distribution = Distribution(None, {3: None, 5: None})
		self.assertEqual(len(list(PacketGenerator.experiment1(6, distribution))), 6)
		self.assertEqual(len(list(PacketGenerator.experiment1(5, distribution))), 5)


if __name__ == '__main__':
	unittest.main()
