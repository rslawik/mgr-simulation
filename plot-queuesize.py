#!/usr/bin/env python3
import sys
from matplotlib import pyplot
from itertools import accumulate

from LogReader import LogReader

if len(sys.argv) != 2:
	print("Usage: {} <simulation.log>".format(sys.argv[0]))
	sys.exit(1)

pyplot.rcParams["figure.figsize"] = [5.75, 4.0]

reader = LogReader(sys.argv[1])

def calculateQueue(packets):
	timeQueue = {}
	sentPackets = filter(lambda pe: pe.successful, packets)
	injects = list(reader.injects)
	queue = {}

	def enqueue(packet):
		if packet not in queue: queue[packet] = 0
		queue[packet] += 1

	def recordInTimeQueue(time):
		for packet in queue:
			if packet not in timeQueue: timeQueue[packet] = []
			timeQueue[packet].append((time, queue[packet]))

	for pe in sentPackets:
		while injects and injects[0][0] <= pe.end:
			enqueue(injects[0][1])
			injects.pop(0)
		queue[pe.packet] -= 1
		recordInTimeQueue(pe.end)

	return timeQueue

l = []
def plotTimeQueue(timeQueue, label):
	for packet in timeQueue:
		tx, = pyplot.plot(*zip(*timeQueue[packet]))
		l.append((tx, "qs($\mathsf{{{0}}}$, {1})".format(label, packet)))


algTimeQueue = calculateQueue(reader.algPackets)
plotTimeQueue(algTimeQueue, "ALG")

advTimeQueue = calculateQueue(reader.advPackets)
plotTimeQueue(advTimeQueue, "ADV")

pyplot.legend(*zip(*l), loc=2)
pyplot.show()
