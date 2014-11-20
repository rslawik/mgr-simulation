#!/usr/bin/env python3
import sys

from Logger import Reader

if len(sys.argv) != 2:
	print("Usage: {} <simulation.log>".format(sys.argv[0]))
	sys.exit(1)

reader = Reader(sys.argv[1])

print(reader.ratios[-1])
