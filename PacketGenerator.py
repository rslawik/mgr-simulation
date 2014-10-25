
def experiment1(n, p1, p2):
	n, p1, p2 = int(n), float(p1), float(p2)
	p1, p2 = min(p1, p2), max(p1, p2)
	time, sent = 0, 0
	while True:
		if sent == n: break
		yield time, p1
		sent += 1

		if sent == n: break
		yield time, p2
		sent += 1

		time += p1 + p2

def stochastic(n, distribution):
	pass

# from random import random, expovariate

# from Distribution import Distribution

# distribution = Distribution.fromFile(sys.argv[1])
# n = int(sys.argv[2])

# def generate(distribution, n):
# 	def randomPacket():
# 		p = random()
# 		for packet in distribution.packets:
# 			p -= distribution.probability(packet)
# 			if p <= 0:
# 				return packet

# 	time = 0.0
# 	for _ in range(n):
# 		yield time, randomPacket()
# 		time += expovariate(distribution.rate)
