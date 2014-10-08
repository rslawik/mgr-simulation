import sys

from Event import InjectEvent
from Events import Events

def play(algorithm, adversary, events):
	time = 0.0

	while events.hasNext():
		event = events.next()
		time = event.time
		print('>>', time, event)

# test play
events = Events([InjectEvent(0.5, None), InjectEvent(1.0, None)])
play(None, None, events)
