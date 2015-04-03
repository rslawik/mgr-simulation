#!/usr/bin/env python3
# should be locate in main directory
import sys

if len(sys.argv) != 3:
	print("{} <model-file> <events-file>".format(sys.argv[0]))
	sys.exit(1)

from matplotlib import pyplot
pyplot.rcParams["figure.figsize"] = [5.75, 2.5]

from Model import Model
from Events import Events

model, events = Model.fromFile(sys.argv[1]), Events.fromFile(sys.argv[2])

count = dict((p, 0) for p in model.packets)
trace = dict((p, []) for p in model.packets)
cumTrace = []

events.next()
while events.hasNext():
	event = events.next()
	time, packet = event.time, event.packet
	count[packet] += 1
	tcount = model.rate * model.probability(packet) * time
	trace[packet].append((time, count[packet], tcount, count[packet] / tcount))

	cumTrace.append((time, sum(count[p] for p in model.packets) / model.rate / time))

lr, = pyplot.plot(list(map(lambda e: e[0], cumTrace)), [1] * len(cumTrace))
lp, = pyplot.plot(*zip(*cumTrace))
pyplot.ylim(0.95, 1.05)
pyplot.ylabel('ratio')
pyplot.xlabel('time')
pyplot.subplots_adjust(bottom=0.2, left=.12, right=.97, top=.99, hspace=.35)

pyplot.show()
