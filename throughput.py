#!/usr/bin/env python3
import sys

from LogReader import LogReader

if len(sys.argv) != 2:
	print("Usage: {} <simulation.log>".format(sys.argv[0]))
	sys.exit(1)

reader = LogReader(sys.argv[1])

isSuccessful = lambda pe: pe.successful
packet = lambda pe: pe.packet
algSent = sum(map(packet, filter(isSuccessful, reader.algPackets)))
advSent = sum(map(packet, filter(isSuccessful, reader.advPackets)))

print(algSent / advSent)
