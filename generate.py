#!/usr/bin/env python3
import sys
import PacketGenerator

if len(sys.argv) != 4 or not hasattr(PacketGenerator, sys.argv[1]):
	print("Usage: {} <generator> <n> <distribution info file>".format(sys.argv[0]))
	sys.exit(1)

from Distribution import Distribution

generator = getattr(PacketGenerator, sys.argv[1])
for time, packet in generator(int(sys.argv[2]), Distribution.fromFile(sys.argv[3])):
	print(time, packet)
