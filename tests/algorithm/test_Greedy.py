class GreedyAlgorithmTestCase(unittest.TestCase):
	def setUp(self):
		distribution = Distribution(3, {1: 0.2, 2: 0.3, 8: 0.5})
		self.algorithm = GreedyAlgorithm(distribution, lambda alg, e: None)

	def testTotalLength_1(self):
		# inject packets
		for packet in [2, 1, 2]:
			self.algorithm.notify(InjectEvent(0, packet))
		totalLength = self.algorithm.totalLength(3)
		self.assertEqual(totalLength, 5)

	def testTotalLength_2(self):
		# inject packets
		for packet in ([1] * 10) + [8]:
			self.algorithm.notify(InjectEvent(0, packet))
		totalLength = self.algorithm.totalLength(3)
		self.assertEqual(totalLength, 18)

	def testSchedule_Nothing(self):
		# inject packets
		for packet in [2, 1, 2]:
			self.algorithm.notify(InjectEvent(0, packet))
		scheduled = self.algorithm.schedule()
		self.assertIsNone(scheduled)

	def testSchedule_Example1(self):
		#inject packets
		for packet in [1, 2] * 4:
			self.algorithm.notify(InjectEvent(0, packet))

		#test schedule
		for testPacket in [1] * 4 + [2] * 2:
			scheduled = self.algorithm.schedule()
			self.assertEqual(scheduled, testPacket)
			self.algorithm.notify(SentEvent(0, self.algorithm, scheduled))

	def testSchedule_Example2(self):
		#inject packets
		for packet in [1] * 2 +  [2] * 4:
			self.algorithm.notify(InjectEvent(0, packet))

		#test schedule
		for testPacket in [1] * 2 + [2] * 3:
			scheduled = self.algorithm.schedule()
			self.assertEqual(scheduled, testPacket)
			self.algorithm.notify(SentEvent(0, self.algorithm, scheduled))

	def testSchedule_Example3(self):
		#inject packets
		for packet in [1] * 2 +  [2] * 4:
			self.algorithm.notify(InjectEvent(0, packet))

		#test schedule
		for testPacket in [1] * 2 + [2] * 3:
			scheduled = self.algorithm.schedule()
			self.assertEqual(scheduled, testPacket)
			self.algorithm.notify(SentEvent(0, self.algorithm, scheduled))

		self.algorithm.notify(InjectEvent(0, 8))

		scheduled = self.algorithm.schedule()
		self.assertEqual(scheduled, 8)
		self.algorithm.notify(SentEvent(0, self.algorithm, scheduled))

		#inject packets
		for packet in [2] * 3:
			self.algorithm.notify(InjectEvent(0, packet))

		#test schedule
		for testPacket in [2] * 4:
			scheduled = self.algorithm.schedule()
			self.assertEqual(scheduled, testPacket)
			self.algorithm.notify(SentEvent(0, self.algorithm, scheduled))
