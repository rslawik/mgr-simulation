class LLAlgorithmTestCase(unittest.TestCase):
	def setUp(self):
		distribution = Distribution(3, {1: 0.5, 2: 0.25, 1.5: 0.25})
		self.algorithm = LLAlgorithm(distribution, lambda ale, e: None)

	def test_schedule(self):
		for testScheduledPacket in [1, 2, 1.5, 1]:
			self.algorithm.notify(InjectEvent(0, testScheduledPacket))
		for testScheduledPacket in [2, 1.5, 1, 1]:
			scheduledPacket = self.algorithm.schedule()
			self.assertEqual(scheduledPacket, testScheduledPacket)
			self.algorithm.notify(SentEvent(0, self.algorithm, scheduledPacket))
