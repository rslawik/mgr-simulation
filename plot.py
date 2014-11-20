#!/usr/bin/env python3
import sys
from matplotlib import pyplot

from Logger import Reader

if len(sys.argv) != 2:
	print("Usage: {} <simulation.log>".format(sys.argv[0]))
	sys.exit(1)

reader = Reader(sys.argv[1])

pyplot.plot(reader.times, reader.ratios)
pyplot.show()
