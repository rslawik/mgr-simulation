#!/usr/bin/env python3
import sys

import Algorithm, Adversary

if len(sys.argv) != 5 or not hasattr(Algorithm, sys.argv[1]) or not hasattr(Adversary, sys.argv[2]):
	print("Usage: {} <algorithm> <adversary> <events file> <distribution info file>".format(sys.argv[0]))
	sys.exit(1)

from Distribution import Distribution
from Event import InjectEvent, SentEvent, ErrorEvent
from Events import Events
from Logger import Logger

def play(algorithm, adversary, events):
	def schedule(algorithm):
		packet = algorithm.schedule()
		if packet: events.schedule(SentEvent(time + packet, algorithm, packet))
		return packet

	while events.hasNext():
		event = events.next()
		time = event.time
		print('>>', event)

		algorithm.notify(event)
		adversary.notify(event)

		if events.hasNextNow(time): continue

		if not algorithm.sending:
			packet = schedule(algorithm)
			error = adversary.scheduleError(packet)
			if error: events.schedule(ErrorEvent(time + error))

		if not adversary.sending: schedule(adversary)

with Logger('alg.log') as alglog, Logger('adv.log') as advlog:
	distribution = Distribution.fromFile(sys.argv[4])
	algorithm = getattr(Algorithm, sys.argv[1])(distribution, alglog.logSent)
	adversary = getattr(Adversary, sys.argv[2])(distribution, advlog.logSent)
	events = Events.fromFile(sys.argv[3])

	play(algorithm, adversary, events)
