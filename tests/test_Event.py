import unittest

from Event import *

class MyTestCase(unittest.TestCase):
	def test_createInjectEvent(self):
		time = 123.07
		event = InjectEvent(time, None)
		self.assertEqual(event.time, time)
	def test_createSentEvent(self):
		time = 123.07
		event = SentEvent(time, None)
		self.assertEqual(event.time, time)
	def test_createErrorEvent(self):
		time = 123.07
		event = ErrorEvent(time)
		self.assertEqual(event.time, time)

if __name__ == '__main__':
	unittest.main()
