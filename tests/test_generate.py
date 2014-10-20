import unittest

class GenerateTestCase(unittest.TestCase):
	def test_exampleGenerate(self):
		packets = {3.0: 0, 5.0: 0, 7.0: 0}
		with open("tests/example/generate.out") as out:
			for line in out:
				_, packet = line.split()
				packets[float(packet)] += 1
		total = sum(packets.values())
		# print(packets, total)
		self.assertEqual(round(packets[3.0]/total, 2), 0.33)
		self.assertEqual(round(packets[5.0]/total, 2), 0.17)
		self.assertEqual(round(packets[7.0]/total, 2), 0.5) 

if __name__ == '__main__':
	unittest.main()
