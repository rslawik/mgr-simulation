import sys

import Algorithm, Adversary

if len(sys.argv) != 4 or not hasattr(Algorithm, sys.argv[1]) or not hasattr(Adversary, sys.argv[2]):
	print("Usage: {} <algorithm> <adversary> <events file>".format(sys.argv[0]))
	sys.exit(1)

from Event import InjectEvent, SentEvent, ErrorEvent
from Events import Events

def play(algorithm, adversary, events):
	def schedule(algorithm):
		packet = algorithm.schedule()
		if packet: events.schedule(SentEvent(time + packet, algorithm))
		return packet

	time = 0.0

	while events.hasNext():
		event = events.next()
		time = event.time
		print('>>', time, event)

		algorithm.notify(event)
		adversary.notify(event)

		if isinstance(event, InjectEvent) and events.hasNextInjectNow(time):
			continue

		if not algorithm.sending:
			packet = schedule(algorithm)
			error = adversary.scheduleError(packet)
			if error: events.schedule(ErrorEvent(time + error))

		if not adversary.sending: schedule(adversary)

algorithm = getattr(Algorithm, sys.argv[1])
adversary = getattr(Adversary, sys.argv[2])
events = Events.fromFile(sys.argv[3])

play(algorithm, adversary, events)
