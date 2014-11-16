#!/usr/bin/env python3
import sys
from matplotlib import pyplot

def readLog(filename, r):
	with open(filename, 'r') as log:
		for entry in log:
			time, packet = map(float, entry.strip().split())
			#print(time, packet)
			if time > 500: break
			pyplot.plot([time-packet, time], [r, r], linewidth=5)

algLog = readLog(sys.argv[1], 1)
advLog = readLog(sys.argv[2], 2)

# pyplot.ylim(ymax=10)
pyplot.yticks([1, 2], ['ALG', 'ADV'])
pyplot.margins(y=1)

pyplot.show()
