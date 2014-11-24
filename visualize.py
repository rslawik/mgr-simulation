#!/usr/bin/env python3
import sys
from matplotlib import pyplot

from Logger import Reader

if len(sys.argv) != 2:
	print("Usage: {} <simulation.log>".format(sys.argv[0]))
	sys.exit(1)

LINEWIDTH = 4
LIMIT = 20
row = {'ALG': -1, 'ADV': 1}
legendmap = {}

def colorGen():
	# yield 'red', 'pink'
	yield 'green', 'orange'
	yield 'blue', 'yellow'
	yield 'violet', 'brown'
	yield 'purple', 'magenta'
colorGenerator = colorGen()

colormap = {}
def getColor(packet, algorithm):
	if (algorithm, packet) not in colormap:
		print("#", algorithm, packet)
		colors = colorGenerator.__next__()
		colormap['ALG', packet] = colors
		colormap['ADV', packet] = colors
	c1, c2 = colormap[algorithm, packet]
	colormap[algorithm, packet] = c2, c1
	return c1


reader = Reader(sys.argv[1])

iteration = 1
for time, algorithm, packet in reader.sentLog:
	if iteration == LIMIT: break
	# print(time, algorithm, packet)
	r = row[algorithm]
	color = getColor(packet, algorithm)
	ret = pyplot.plot([time-packet, time], [r, r], linewidth=LINEWIDTH, color=color, label=str(packet))
	legendmap[packet, color] = ret
	iteration += 1


iteration = 1
for time in reader.errorLog:
	if iteration == LIMIT: break
	pyplot.plot([time, time], [-1, 1], '--', linewidth=LINEWIDTH/2, color='grey')
	iteration += 1

# pyplot.ylim(ymax=10)
pyplot.yticks([-1, 1], ['ALG', 'ADV'])
pyplot.ylim(-2, 2)
#pyplot.ylim(-15, 15)
#pyplot.margins(ymargin=0.5, ymin=5)
pyplot.legend(map(lambda l: legendmap[l][0], legendmap.keys()), map(lambda l: l[0], legendmap.keys()))

pyplot.show()
