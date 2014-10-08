import unittest

from Event import Event
from Events import Events

class EventsTestCase(unittest.TestCase):
	def setUp(self):
		self.events = Events()

	def test_createEvents(self):
		self.assertEqual(self.events.hasNext(), False)

	def test_canScheduleEvent(self):
		event = Event(1.1)
		self.events.schedule(event)
		self.assertEqual(self.events.hasNext(), True)

if __name__ == '__main__':
	unittest.main()
