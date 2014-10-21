import unittest

from Event import InjectEvent, SentEvent, ErrorEvent
from Events import Events

class EmptyEventsTestCase(unittest.TestCase):
	def setUp(self):
		self.events = Events([])

	def test_createEvents(self):
		self.assertEqual(self.events.hasNext(), False)

	def test_canScheduleEvent(self):
		event = SentEvent(1.1, None)
		self.events.schedule(event)
		self.assertEqual(self.events.hasNext(), True)

	def test_canGetNextEvent(self):
		event = SentEvent(1.2, None)
		self.events.schedule(event)
		nextEvent = self.events.next()
		self.assertEqual(nextEvent, event)

	def test_cannotGetNextEventFromEmpty(self):
		self.assertRaises(IndexError, self.events.next)

	def test_canGetNextEventsInOrder(self):
		e1, e2, e3 = SentEvent(4.3, None), SentEvent(7.1, None), SentEvent(2.3, None)
		for e in [e1, e2, e3]: self.events.schedule(e)
		for e in [e3, e1, e2]:
			self.assertEqual(self.events.hasNext(), True)
			nextEvent = self.events.next()
			self.assertEqual(nextEvent, e)
		self.assertEqual(self.events.hasNext(), False)

class EventsTestCase(unittest.TestCase):
	def setUp(self):
		self.ie1, self.ie2, self.ie3 = InjectEvent(1.1, None), InjectEvent(4.2, None), InjectEvent(5.9, None)
		self.events = Events([self.ie1, self.ie2, self.ie3])

	def test_createEvents(self):
		self.assertEqual(self.events.hasNext(), True)

	def assertHasEventsInOrder(self, order):
		for e in order:
			self.assertEqual(self.events.hasNext(), True)
			ne = self.events.next()
			self.assertEqual(ne, e)

	def test_canScheduleSentEvent(self):
		event = SentEvent(2.7, None)
		self.events.schedule(event)
		self.assertHasEventsInOrder([self.ie1, event, self.ie2, self.ie3])

	def test_canScheduleSentAndErrorEvent(self):
		sentEvent, errorEvent = SentEvent(2.7, None), ErrorEvent(2.8)
		self.events.schedule(sentEvent)
		self.events.schedule(errorEvent)
		self.assertHasEventsInOrder([self.ie1, sentEvent, self.ie2, self.ie3])

	def test_canScheduleSentAndErrorEventBefore(self):
		sentEvent, errorEvent = SentEvent(2.9, None), ErrorEvent(2.8)
		self.events.schedule(sentEvent)
		self.events.schedule(errorEvent)
		self.assertHasEventsInOrder([self.ie1, self.ie2, self.ie3])

	def test_canGetNextEventInjectBeforeSent(self):
		se = SentEvent(4.2, None)
		self.events.schedule(se)
		self.assertHasEventsInOrder([self.ie1, self.ie2, se, self.ie3])

class SimultaneousEventsTestCase(unittest.TestCase):
	def test_withSimultaneousEvents(self):
		ie1, ie2 = InjectEvent(1, None), InjectEvent(1, None)
		events = Events([ie1, ie2])
		nextEvent = events.next()
		self.assertTrue(events.hasNextInjectNow(nextEvent.time))

	def test_withoutSimultaneousEvents(self):
		ie1, ie2 = InjectEvent(1, None), InjectEvent(2, None)
		events = Events([ie1, ie2])
		nextEvent = events.next()
		self.assertFalse(events.hasNextInjectNow(nextEvent.time))

class EventsFromFileTestCase(unittest.TestCase):
	def test_eventsFromFileNoFile(self):
		with self.assertRaises(FileNotFoundError):
			events = Events.fromFile('tests/example/events.inXXX')

	def test_eventsFromFile(self):
		events = Events.fromFile('tests/example/events.in')
		self.assertEqual(events.next().time, 1)
		self.assertEqual(events.next().time, 2)
		self.assertEqual(events.next().packet, 3)
		self.assertEqual(events.next().packet, 4)
		self.assertEqual(events.next().time, 5)
		self.assertTrue(events.hasNextInjectNow(5))
		self.assertEqual(events.next().packet, 4)

if __name__ == '__main__':
	unittest.main()
