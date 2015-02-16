#!/usr/bin/env python3
import sys

import Algorithm, Adversary

if len(sys.argv) != 5 or not hasattr(Algorithm, sys.argv[1]) or not hasattr(Adversary, sys.argv[2]):
	print("Usage: {} <algorithm> <adversary> <events file> <model file>".format(sys.argv[0]))
	sys.exit(1)

from Model import Model
from Event import InjectEvent, SentEvent, ErrorEvent, ScheduleEvent, WaitEvent
from Events import Events

def log(event):
	print(event)

def play(algorithm, adversary, events):
	def schedule(algorithm):
		packet = algorithm.schedule()
		if packet:
			events.schedule(SentEvent(time + packet, algorithm))
			log(ScheduleEvent(time, algorithm, packet))
		return packet

	def scheduleError(time, error):
		if error:
			events.schedule(ErrorEvent(time + error) if error > 0 else WaitEvent())

	while events.hasNext():
		event = events.next()
		time = event.time
		log(event)

		algorithm.notify(event)
		adversary.notify(event)

		if events.hasNextNow(time): continue

		if not algorithm.sending:
			packet = schedule(algorithm)
			error = adversary.algorithmSchedules(packet)
			scheduleError(time, error)

		if not adversary.sending:
			advpacket = schedule(adversary)
			error = adversary.adversarySchedules(advpacket)
			scheduleError(time, error)

model = Model.fromFile(sys.argv[4])
algorithm = getattr(Algorithm, sys.argv[1])(model)
adversary = getattr(Adversary, sys.argv[2])(model)
events = Events.fromFile(sys.argv[3])

play(algorithm, adversary, events)
