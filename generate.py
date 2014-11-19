#!/usr/bin/env python3
import sys
import PacketGenerator

if len(sys.argv) != 4 or not hasattr(PacketGenerator, sys.argv[1]):
	print("Usage: {} <generator> <n> <model file>".format(sys.argv[0]))
	sys.exit(1)

from Model import Model

generator = getattr(PacketGenerator, sys.argv[1])
n = int(sys.argv[2])
model = Model.fromFile(sys.argv[3])

for time, packet in generator(n, model):
	print(time, packet)
