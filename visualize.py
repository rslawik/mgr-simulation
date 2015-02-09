#!/usr/bin/env python3
import sys
from matplotlib import patches
from matplotlib import pyplot
from random import shuffle

from LogReader import LogReader

if len(sys.argv) != 2 and len(sys.argv) != 3:
	print("Usage: {} <simulation.log> [limit]".format(sys.argv[0]))
	sys.exit(1)

LINEWIDTH = 2
ROW = {"ALG" : 1, "ADV": -1}
COLORS = ["brown", "orange", "pink", "magenta", "yellow", "red", "green", "blue", "purple"]
shuffle(COLORS)

limit = float(sys.argv[2]) if len(sys.argv) > 2 else None
reader = LogReader(sys.argv[1], limit=limit)

colormap = {}
colorlegend = []
def chooseColor(length):
	if length not in colormap:
		color = COLORS.pop()
		colormap[length] = color
		colorPatch = patches.Patch(color=color, label=str(length))
		colorlegend.append(colorPatch)
	return colormap[length]

def plotPacket(algorithm, packetEntry):
	y = ROW[algorithm]
	length = packetEntry.end - packetEntry.start
	color = chooseColor(packetEntry.packet)
	eb = pyplot.errorbar(packetEntry.start, y, xerr=[[0], [length]], capsize=10, capthick=LINEWIDTH, linewidth=LINEWIDTH, ecolor=color)
	eb[-1][0].set_linestyle('-' if packetEntry.successful else '--')

def plotError(time):
	pyplot.plot([time, time], [-1, 1], '--', linewidth=LINEWIDTH, color='grey')

for packetEntry in reader.algPackets:
	plotPacket("ALG", packetEntry)

for packetEntry in reader.advPackets:
	plotPacket("ADV", packetEntry)

for time in reader.errors:
	plotError(time)

pyplot.yticks([-1, 1], ['ADV', 'ALG'])
pyplot.ylim(-4, 4)
pyplot.legend(handles=colorlegend)

pyplot.show()
