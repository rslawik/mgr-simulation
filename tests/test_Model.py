import unittest

from Model import Model

class ModelTestCase(unittest.TestCase):
	def test_createModel(self):
		rate, distribution = 3, {1: 0.5, 2: 0.25, 1.5: 0.25}
		model = Model(rate, distribution)
		self.assertModelEqual(model, rate, distribution)

	def assertModelEqual(self, model, rate, distribution):
		packets = sorted(distribution.keys())

		self.assertEqual(model.packets, packets)
		self.assertEqual(model.rate, rate)
		for packet in packets:
			self.assertEqual(model.probability(packet), distribution[packet])

class InvalidModelTestCase(ModelTestCase):
	def test_createModel(self):
		with self.assertRaises(AssertionError):
			rate, distribution = 3, {1: 0.5, 2: 0.25}
			model = Model(rate, distribution)

class ModelFromFileTestCase(ModelTestCase):
	def test_createModel_NoFile(self):
		with self.assertRaises(FileNotFoundError):
			model = Model.fromFile('tests/example/modelXXX.in')

	def test_createModel(self):
		model = Model.fromFile('tests/example/model1.in')
		self.assertModelEqual(model, 5, {3.0: 0.33, 5.0: 0.17, 7.0: 0.5})

	def test_createDistributionWithoutInfo(self):
		model = Model.fromFile('tests/example/model2.in')
		self.assertModelEqual(model, None, {3.0: None, 5.0: None, 7.0: None})
