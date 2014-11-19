import unittest

import PacketGenerator
from Model import Model

class PacketGeneratorTestCase(unittest.TestCase):
	def test_experiment1iteration(self):
		model = Model.withPackets(3, 5)
		expected = [(0, 3), (0, 5), (8, 3), (8, 5), (16, 3), (16, 5)]
		generator = PacketGenerator.experiment1(6, model)
		for ie, eic in zip(generator, expected):
			self.assertEqual(ie, eic)

	def test_experiment1length(self):
		model = Model.withPackets(3, 5)
		self.assertEqual(len(list(PacketGenerator.experiment1(6, model))), 6)
		self.assertEqual(len(list(PacketGenerator.experiment1(5, model))), 5)
