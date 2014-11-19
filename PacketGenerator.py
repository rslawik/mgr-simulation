from random import random, expovariate

def sirocco_thm9(n, model):
	assert len(model.packets) == 2
	p1, p2 = model.packets
	time, sent = 0, 0
	while True:
		if sent == n: break
		yield time, p1
		sent += 1

		if sent == n: break
		yield time, p2
		sent += 1

		time += p1 + p2

def stochastic(n, model):
	def randomPacket():
		p = random()
		for packet in model.packets:
			p -= model.probability(packet)
			if p <= 0:
				return packet

	time = 0.0
	for _ in range(n):
		yield time, randomPacket()
		time += expovariate(model.rate)
