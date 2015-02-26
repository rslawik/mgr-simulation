#!/usr/bin/env python3
import sys
from matplotlib import pyplot
from itertools import accumulate

from LogReader import LogReader

if len(sys.argv) != 2 and len(sys.argv) != 3:
	print("Usage: {} <simulation.log> [expected-value]".format(sys.argv[0]))
	sys.exit(1)

pyplot.rcParams["figure.figsize"] = [5.75, 4.0]

reader = LogReader(sys.argv[1])

def calculateSent(packets):
	sentPackets = list(filter(lambda pe: pe.successful, packets))
	return list(zip(map(lambda pe: pe.end, sentPackets), accumulate(map(lambda pe: pe.packet, sentPackets))))

algSent, advSent = calculateSent(reader.algPackets), calculateSent(reader.advPackets)

times, ratios = [], []
sAlg = 0.0
for t, sAdv in advSent:
	while algSent and algSent[0][0] <= t:
		sAlg = algSent.pop(0)[1]
	times.append(t)
	ratios.append(sAlg / sAdv)

tx, = pyplot.plot(times, ratios)
l = [(tx, "$T_\mathsf{ALG}$")]
if len(sys.argv) == 3:
	expected = float(sys.argv[2])
	te, = pyplot.plot(times, [expected] * len(times))
	l.append((te, "expected"))
# pyplot.ylim(0, 1)
pyplot.legend(*zip(*l), loc=4)
pyplot.show()
