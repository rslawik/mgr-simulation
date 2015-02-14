import unittest

from Event import *

class EventTestCase(unittest.TestCase):
	def test_createInjectEvent(self):
		time = 123.07
		event = InjectEvent(time, None)
		self.assertEqual(event.time, time)

	def test_createInjectEvent(self):
		event = InjectEvent.fromLine("123.07 4.23")
		self.assertEqual(event.time, 123.07)
		self.assertEqual(event.packet, 4.23)

	def test_createSentEvent(self):
		time = 123.07
		event = SentEvent(time, None)
		self.assertEqual(event.time, time)

	def test_createErrorEvent(self):
		time = 123.07
		event = ErrorEvent(time)
		self.assertEqual(event.time, time)

	def test_createMultipleEvents(self):
		e1, e2, e3 = InjectEvent(1, None), SentEvent(2, None), ErrorEvent(3)
		self.assertNotEqual(e1.time, e2.time)
		self.assertNotEqual(e1.time, e3.time)
		self.assertNotEqual(e2.time, e3.time)
	
	def test_orderEvent(self):
		e1, e2 = InjectEvent(1, None), ErrorEvent(2)
		self.assertEqual(e1 < e2, True)

if __name__ == '__main__':
	print("TestEvent")
	unittest.main()
