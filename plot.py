#!/usr/bin/env python3
import sys
from collections import deque
from matplotlib import pyplot

def readLog(filename):
	times, totals = [0.0], [0.0]
	with open(filename, 'r') as log:
		for entry in log:
			time, packet = entry.strip().split()
			times.append(float(time))
			totals.append(totals[-1] + float(packet))
	return zip(times, totals)

def merge(algorithmLog, adversaryLog):
	algorithmLog, adversaryLog = deque(algorithmLog), deque(adversaryLog)
	time, algSent, advSent = 0.0, 0.0, 0.0
	times, ratios = [], []

	def append():
		times.append(time)
		ratios.append(algSent / advSent if advSent > 0 else 1.0)

	while algorithmLog and adversaryLog:
		time = min(algorithmLog[0][0], adversaryLog[0][0])
		if algorithmLog[0][0] == time:
			_, algSent = algorithmLog.popleft()
		if adversaryLog[0][0] == time:
			_, advSent = adversaryLog.popleft()
		append()

	while algorithmLog:
		time, algSent = algorithmLog.popleft()
		append()

	while adversaryLog:
		time, advSent = adversaryLog.popleft()
		append()

	return times, ratios

algorithmLog = readLog(sys.argv[1])
adversaryLog = readLog(sys.argv[2])

log = merge(algorithmLog, adversaryLog)

pyplot.plot(*log)
pyplot.show()
