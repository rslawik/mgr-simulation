import unittest

from Model import Model
from Algorithm import SL, LL, SLPreamble, Greedy, Prudent
from Event import InjectEvent, SentEvent, ErrorEvent

class AlgorithmTestCase(unittest.TestCase):
	def injectPackets(self, *packets):
		for packet in packets:
			self.algorithm.notify(InjectEvent(0, packet))

	def assertSchedulePackets(self, packets):
		for packet in packets:
			scheduled = self.algorithm.schedule()
			self.assertEqual(scheduled, packet)
			self.algorithm.notify(SentEvent(0, self.algorithm, scheduled))

	def assertScheduleAndError(self, packet):
		scheduled = self.algorithm.schedule()
		self.assertEqual(scheduled, packet)
		self.algorithm.notify(ErrorEvent(0))

class SLTestCase(AlgorithmTestCase):
	def setUp(self):
		model = Model.withPackets(1, 2, 1.5)
		self.algorithm = SL(model)

	def test_schedule_1(self):
		self.injectPackets(1, 2, 1.5, 1)
		self.assertSchedulePackets([1, 1, 1.5, 2])

	def test_schedule_2(self):
		self.injectPackets(1, 2, 1.5, 1)
		self.assertScheduleAndError(1)
		self.assertSchedulePackets([1])
		self.assertScheduleAndError(1)
		self.assertSchedulePackets([1, 1.5])
		self.assertScheduleAndError(2)
		self.assertSchedulePackets([2])

class LLAlgorithmTestCase(AlgorithmTestCase):
	def setUp(self):
		model = Model.withPackets(1, 2, 1.5)
		self.algorithm = LL(model)

	def test_schedule_1(self):
		self.injectPackets(1, 2, 1.5, 1)
		self.assertSchedulePackets([2, 1.5, 1, 1])

	def test_schedule_2(self):
		self.injectPackets(1, 2, 1.5, 1)
		self.assertScheduleAndError(2)
		self.assertScheduleAndError(2)
		self.assertSchedulePackets([2, 1.5])
		self.assertScheduleAndError(1)
		self.assertSchedulePackets([1])
		self.assertScheduleAndError(1)
		self.assertSchedulePackets([1])

class SLPreambleTestCase(AlgorithmTestCase):
	def setUp(self):
		model = Model.withPackets(1, 2)
		self.algorithm = SLPreamble(model)

	def test_schedule_1(self):
		packets = [1, 1, 2, 2, 1, 1]
		self.injectPackets(*packets)
		self.assertSchedulePackets(packets)

	def test_schedule_2(self):
		packets = [2, 2, 2, 1]
		self.injectPackets(*packets)
		self.assertSchedulePackets(packets)

	def test_schedule_3(self):
		packets = [1, 1, 2, 2]
		self.injectPackets(*packets)
		self.assertScheduleAndError(1)
		self.assertSchedulePackets([1])
		self.assertScheduleAndError(1)
		self.assertScheduleAndError(2)
		self.assertScheduleAndError(2)
		self.assertSchedulePackets([2, 2])

	def test_schedule_4(self):
		self.injectPackets(2, 2, 1)
		self.assertSchedulePackets([2])
		self.injectPackets(1, 1, 1)
		self.assertScheduleAndError(2)
		self.assertScheduleAndError(1)
		self.assertSchedulePackets([1, 1])
		self.assertScheduleAndError(2)
		self.assertSchedulePackets([1, 1])

class GreedyTestCase(AlgorithmTestCase):
	def setUp(self):
		model = Model.withPackets(1, 2, 8)
		self.algorithm = Greedy(model)

	def test_totalLength_1(self):
		self.injectPackets(2, 1, 2)
		totalLength = self.algorithm.totalLength(3)
		self.assertEqual(totalLength, 5)

	def test_totalLength_2(self):
		packets = [1] * 10 + [8]
		self.injectPackets(*packets)
		totalLength = self.algorithm.totalLength(2)
		self.assertEqual(totalLength, 10)

	def test_schedule_nothing(self):
		self.injectPackets(2, 1, 2)
		scheduled = self.algorithm.schedule()
		self.assertIsNone(scheduled)

	def test_schedule_1(self):
		packets = [1, 2] * 4
		self.injectPackets(*packets)
		self.assertSchedulePackets([1] * 4 + [2] * 2)

	def test_schedule_2(self):
		packets = [1, 2] * 2 + [2] * 2
		self.injectPackets(*packets)
		self.assertSchedulePackets([1] * 2 + [2] * 3)

	def test_schedule_3(self):
		self.test_schedule_2()
		self.injectPackets(8)
		self.assertSchedulePackets([8])
		self.injectPackets(2, 2, 2)
		self.assertSchedulePackets([2] * 4)

	def test_schedule_4(self):
		packets = [1] * 8 + [2] * 4 + [8]
		self.injectPackets(*packets)
		self.assertSchedulePackets(packets)

# 	def test_canScheduleNextPacketAfterError(self):
# 		self.algorithm.notify(InjectEvent(1, 1))
# 		self.algorithm.notify(InjectEvent(2, 2))
# 		self.algorithm.schedulePacket(1)
# 		self.algorithm.notify(ErrorEvent(2))
# 		self.algorithm.schedulePacket(1)
# 		self.algorithm.notify(SentEvent(2, self.algorithm, 1))
# 		self.algorithm.schedulePacket(2)

class PrudentTestCase(AlgorithmTestCase):
	def setUp(self):
		model = Model.withPackets(1, 2, 8, 16)
		self.algorithm = Prudent(model)

	def test_selectToSend_1(self):
		packets = [1] * 8
		self.injectPackets(*packets)
		toSend = self.algorithm.selectToSend(8, 2)
		self.assertEqual([1], toSend)

	def test_selectToSend_2(self):
		packets = [1] * 17 + [2] * 9
		self.injectPackets(*packets)
		toSend = self.algorithm.selectToSend(16, 2)
		self.assertEqual([1, 2], toSend)

def test_selectToSend_3(self):
		packets = [1] * 10 + [2] * 20 + [8] * 7 + [16] * 3
		self.injectPackets(*packets)
		toSend = self.algorithm.selectToSend(8, 2)
		self.assertEqual([1], toSend)