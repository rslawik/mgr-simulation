import unittest

from Algorithm import Algorithm, SLAlgorithm, LLAlgorithm
from Distribution import Distribution
from Event import InjectEvent, SentEvent, ErrorEvent

class AlgorithmTestCase(unittest.TestCase):
	def setUp(self):
		distribution = Distribution(3, {1: 0.5, 2: 0.25, 1.5: 0.25})
		self.algorithm = Algorithm(distribution)

	def test_createAlgorithm(self):
		self.assertFalse(self.algorithm.sending)

	def test_cannotSchedulePacketNotFromQueue(self):
		with self.assertRaises(AssertionError):
			self.algorithm.schedulePacket(1)

	def test_canSchedulePacketFromQueue(self):
		self.algorithm.notify(InjectEvent(1, 1))
		scheduledPacket = self.algorithm.schedulePacket(1)
		self.assertEqual(scheduledPacket, 1)
		self.assertEqual(self.algorithm.sending, 1)

	def test_canAndCannotSchedulePacketFromQueue(self):
		self.test_canSchedulePacketFromQueue()
		self.test_cannotSchedulePacketNotFromQueue()

	def test_canScheduleNextPacket(self):
		self.algorithm.notify(InjectEvent(1, 1))
		self.algorithm.notify(InjectEvent(2, 2))
		self.algorithm.schedulePacket(1)
		self.algorithm.notify(SentEvent(2, self.algorithm))
		self.algorithm.schedulePacket(2)

	def test_canScheduleNextPacketAfterError(self):
		self.algorithm.notify(InjectEvent(1, 1))
		self.algorithm.notify(InjectEvent(2, 2))
		self.algorithm.schedulePacket(1)
		self.algorithm.notify(ErrorEvent(2))
		self.algorithm.schedulePacket(1)
		self.algorithm.notify(SentEvent(2, self.algorithm))
		self.algorithm.schedulePacket(2)

class SLAlgorithmTestCase(unittest.TestCase):
	def setUp(self):
		distribution = Distribution(3, {1: 0.5, 2: 0.25, 1.5: 0.25})
		self.algorithm = SLAlgorithm(distribution)

	def test_schedule(self):
		for testScheduledPacket in [1, 2, 1.5, 1]:
			self.algorithm.notify(InjectEvent(0, testScheduledPacket))
		for testScheduledPacket in [1, 1, 1.5, 2]:
			scheduledPacket = self.algorithm.schedule()
			self.assertEqual(scheduledPacket, testScheduledPacket)
			self.algorithm.notify(SentEvent(0, self.algorithm))

class LLAlgorithmTestCase(unittest.TestCase):
	def setUp(self):
		distribution = Distribution(3, {1: 0.5, 2: 0.25, 1.5: 0.25})
		self.algorithm = LLAlgorithm(distribution)

	def test_schedule(self):
		for testScheduledPacket in [1, 2, 1.5, 1]:
			self.algorithm.notify(InjectEvent(0, testScheduledPacket))
		for testScheduledPacket in [2, 1.5, 1, 1]:
			scheduledPacket = self.algorithm.schedule()
			self.assertEqual(scheduledPacket, testScheduledPacket)
			self.algorithm.notify(SentEvent(0, self.algorithm))	

if __name__ == '__main__':
	unittest.main()
