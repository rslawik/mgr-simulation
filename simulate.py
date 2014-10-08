import sys

from Algorithm import Algorithm
from Adversary import Adversary
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

		if not algorithm.sending:
			packet = schedule(algorithm)
			error = adversary.scheduleError(packet)
			if error: events.schedule(ErrorEvent(time + error))

		if not adversary.sending: schedule(adversary)

# test play
events = Events([InjectEvent(0.5, None), InjectEvent(1.0, None)])
algorithm = Algorithm()
adversary = Adversary()

play(algorithm, adversary, events)
