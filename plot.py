import sys
from matplotlib import pyplot

def readLog(filename):
	times, total = [0.0], [0.0]
	with open(filename, 'r') as log:
		for entry in log:
			time, packet = entry.strip().split()
			times.append(float(time))
			total.append(total[-1] + float(packet))
	return times, total

def merge(algorithmLog, adversaryLog):
	algTimes, algTotal = algorithmLog
	advTimes, advTotal = adversaryLog
	algSent, advSent = 0.0, 0.0
	times, total = [0.0], [0.0]
	# TODO
	return times, total

algorithmLog = readLog(sys.argv[1])
adversaryLog = readLog(sys.argv[2])

log = merge(algorithmLog, adversaryLog)

pyplot.plot(*log)
pyplot.show()