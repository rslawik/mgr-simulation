import sys
from random import random, expovariate

from Distribution import Distribution

distribution = Distribution.fromFile(sys.argv[1])
n = int(sys.argv[2])

def generate(distribution, n):
	def randomPacket():
		p = random()
		for packet in distribution.packets:
			p -= distribution.probability(packet)
			if p <= 0:
				return packet

	time = 0.0
	for _ in range(n):
		yield time, randomPacket()
		time += expovariate(distribution.rate)


for time, packet in generate(distribution, n):
	print(time, packet)
