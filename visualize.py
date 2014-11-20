#!/usr/bin/env python3
import sys
from matplotlib import pyplot

from Logger import Reader

LINEWIDTH = 10

if len(sys.argv) != 2:
	print("Usage: {} <simulation.log>".format(sys.argv[0]))
	sys.exit(1)

reader = Reader(sys.argv[1])

row = {'ALG': 1, 'ADV': 2}
colors, c = ['red', 'green', 'blue', 'yellow'], 0
colormap = {}
legendmap = {}

for time, algorithm, packet in reader.sentLog:
	# print(time, algorithm, packet)
	r = row[algorithm]
	if packet not in colormap:
		colormap[packet] = colors[c]
		c += 1
	color = colormap[packet]
	ret = pyplot.plot([time-packet, time], [r, r], linewidth=LINEWIDTH, color=color, label=str(packet))
	legendmap[packet] = ret

for time in reader.errorLog:
	pyplot.plot([time, time], [1, 2], '--', linewidth=LINEWIDTH/2, color='grey')

packets = list(colormap.keys())

# pyplot.ylim(ymax=10)
pyplot.yticks([1, 2], ['ALG', 'ADV'])
pyplot.margins(y=1)
pyplot.legend(map(lambda p: legendmap[p][0], packets), packets)

pyplot.show()
