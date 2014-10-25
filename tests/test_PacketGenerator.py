import unittest

import PacketGenerator

class PacketGeneratorTestCase(unittest.TestCase):
	def test_experiment1iteration(self):
		expected = [(0, 3), (0, 5), (8, 3), (8, 5), (16, 3), (16, 5)]
		generator = PacketGenerator.experiment1(6, 5, 3)
		for ie, eic in zip(generator, expected):
			self.assertEqual(ie, eic)

	def test_experiment1length(self):
		self.assertEqual(len(list(PacketGenerator.experiment1(6, 3, 5))), 6)
		self.assertEqual(len(list(PacketGenerator.experiment1(5, 1, 2))), 5)


if __name__ == '__main__':
	unittest.main()
