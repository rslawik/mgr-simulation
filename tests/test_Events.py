import unittest

from Event import InjectEvent, SentEvent, ErrorEvent
from Events import Events

class EmptyEventsTestCase(unittest.TestCase):
	def setUp(self):
		self.events = Events([])

	def test_createEvents(self):
		self.assertEqual(self.events.hasNext(), False)

	def test_canScheduleEvent(self):
		event = SentEvent(1.1, None, None)
		self.events.schedule(event)
		self.assertEqual(self.events.hasNext(), True)

	def test_canGetNextScheduledEvent(self):
		event = SentEvent(1.2, None, None)
		self.events.schedule(event)
		nextEvent = self.events.next()
		self.assertEqual(nextEvent, event)

	def test_cannotGetNextEventFromEmpty(self):
		self.assertEqual(self.events.next(), None)

	def test_canGetNextEventsInOrder(self):
		e1, e2, e3 = SentEvent(4.3, None, None), SentEvent(7.1, None, None), SentEvent(2.3, None, None)
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
		event = SentEvent(2.7, None, None)
		self.events.schedule(event)
		self.assertHasEventsInOrder([self.ie1, event, self.ie2, self.ie3])

	def test_canScheduleSentAndErrorEvent(self):
		sentEvent, errorEvent = SentEvent(2.7, None, None), ErrorEvent(2.8)
		self.events.schedule(sentEvent)
		self.events.schedule(errorEvent)
		self.assertHasEventsInOrder([self.ie1, sentEvent, errorEvent, self.ie2, self.ie3])

	def test_canScheduleSentAndErrorEventBefore(self):
		sentEvent, errorEvent = SentEvent(2.9, None, None), ErrorEvent(2.8)
		self.events.schedule(sentEvent)
		self.events.schedule(errorEvent)
		self.assertHasEventsInOrder([self.ie1, errorEvent, self.ie2, self.ie3])

	def test_canGetNextEventInjectBeforeSent(self):
		se = SentEvent(4.2, None, None)
		self.events.schedule(se)
		self.assertHasEventsInOrder([self.ie1, self.ie2, se, self.ie3])

class SimultaneousEventsTestCase(unittest.TestCase):
	def test_withSimultaneousEvents(self):
		ie1, ie2 = InjectEvent(1, None), InjectEvent(1, None)
		events = Events([ie1, ie2])
		nextEvent = events.next()
		self.assertTrue(events.hasNextNow(nextEvent.time))

	def test_withoutSimultaneousEvents(self):
		ie1, ie2 = InjectEvent(1, None), InjectEvent(2, None)
		events = Events([ie1, ie2])
		nextEvent = events.next()
		self.assertFalse(events.hasNextNow(nextEvent.time))

	def test_SimultaneousSentAndError(self):
		ie1, ie2 = InjectEvent(1, None), InjectEvent(2, None)
		events = Events([ie1, ie2])
		se1 = SentEvent(1.5, None, None)
		events.schedule(se1)
		se2 = SentEvent(2, None, None)
		events.schedule(se2)
		ee = ErrorEvent(1.5)
		events.schedule(ee)
		self.assertEqual(events.next(), ie1)
		self.assertEqual(events.next(), se1)
		self.assertEqual(events.next(), ee)
		self.assertEqual(events.next(), ie2)
		self.assertEqual(events.hasNext(), False)

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
		self.assertTrue(events.hasNextNow(5))
		self.assertEqual(events.next().packet, 4)

class Experiment1TestCase(unittest.TestCase):
	def test_canPerformExperiment1(self):
		# t=0
		ie1, ie2 = InjectEvent(0, 3), InjectEvent(0, 5)
		events = Events([ie1, ie2])
		self.assertEqual(events.next(), ie1)
		self.assertEqual(events.next(), ie2)
		se1, se2 = SentEvent(3, "alg", 3), SentEvent(5, "adv", 5)
		events.schedule(se1)
		events.schedule(se2)
		ee1 = ErrorEvent(5)
		events.schedule(ee1)
		# t=3
		self.assertEqual(events.next(), se1)
		se3 = SentEvent(8, "alg", 5)
		events.schedule(se3)
		ee2 = ErrorEvent(8)
		events.schedule(ee2)
		# t=5
		self.assertEqual(events.next(), se2)
		self.assertEqual(events.next(), ee1)
		se4 = SentEvent(8, "adv", 3)
		events.schedule(se4)
		# t=8
		self.assertEqual(events.next(), se4)
		self.assertEqual(events.next(), ee2)
		self.assertFalse(events.hasNext())



if __name__ == '__main__':
	unittest.main()
