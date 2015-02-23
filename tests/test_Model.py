import unittest

from Model import Model

class ModelTestCase(unittest.TestCase):
	def assertModelEqual(self, model, rate, distribution, speedup):
		packets = sorted(distribution.keys())

		self.assertEqual(model.packets, packets)
		self.assertEqual(model.rate, rate)
		for packet in packets:
			self.assertEqual(model.probability(packet), distribution[packet])
		self.assertEqual(model.speedup, speedup)

	def test_createModel(self):
		rate, distribution, speedup = 3, {1: 0.5, 2: 0.25, 1.5: 0.25}, 1.0
		model = Model(rate, distribution, speedup)
		self.assertModelEqual(model, rate, distribution, speedup)

	def test_createInvalidModel_rate(self):
		with self.assertRaises(AssertionError):
			model = Model(-1.7, {1: 1.0}, 1.0)

	def test_createInvalidModel_distribution(self):
		with self.assertRaises(AssertionError):
			model = Model(3, {1: 0.5, 2: 0.25}, 1.0)

	def test_createInvalidModel_speedup(self):
		with self.assertRaises(AssertionError):
			model = Model(3, {1: 1.0}, 0.75)

	def test_createModelFromFile(self):
		model = Model.fromFile('tests/example/model.in')
		self.assertModelEqual(model, 5, {3.0: 0.33, 5.0: 0.17, 7.0: 0.5}, 1.5)	

	def test_createModelFromFile_noFile(self):
		with self.assertRaises(FileNotFoundError):
			model = Model.fromFile('tests/example/modelXXX.in')

	def test_createModelWithPackets(self):
		packets = [1, 2]
		model = Model.withPackets(*packets)
		self.assertModelEqual(model, 0.0, {1.0: 0.5, 2.0: 0.5}, 1.0)