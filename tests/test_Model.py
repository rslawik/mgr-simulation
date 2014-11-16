import unittest

from Model import Model

class InvalidModelTestCase(unittest.TestCase):
	def test_createModel(self):
		with self.assertRaises(AssertionError):
			rate, distribution = 3, {1: 0.5, 2: 0.25}
			model = Model(rate, distribution)

class ModelTestCase(unittest.TestCase):
	def setUp(self):
		self.rate, self.distribution = 3, {1: 0.5, 2: 0.25, 1.5: 0.25}
		self.model = Model(self.rate, self.distribution)

	def test_createModel(self):
		self.assertEqual(self.model.rate, self.rate)
		self.assertEqual(self.model.probability(1), self.distribution[1])
		self.assertEqual(self.model.probability(2), self.distribution[2])

	def test_getPacktes(self):
		self.assertEqual(self.model.packets, [1, 1.5, 2])

class ModelFromFileTestCase(unittest.TestCase):
	def test_createModel_NoFile(self):
		with self.assertRaises(FileNotFoundError):
			model = Model.fromFile('tests/example/model.inXXX')

	def test_createModel(self):
		model = Model.fromFile('tests/example/model.in1')
		self.assertEqual(model.packets, [3, 5, 7])
		self.assertEqual(model.rate, 5)
		self.assertEqual(model.probability(3.0), 0.33)
		self.assertEqual(model.probability(5.0), 0.17)
		self.assertEqual(model.probability(7.0), 0.5)

	def test_createDistributionWithoutInfo(self):
		model = Model.fromFile('tests/example/model.in2')
		self.assertEqual(model.packets, [3, 5, 7])
		self.assertEqual(model.rate, None)
		self.assertEqual(model.probability(5.0), None)
