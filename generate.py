import sys
from random import random, expovariate

filename = sys.argv[1]
n = int(sys.argv[2])

with open(filename, 'r') as distributionfile:
	pass

# def next_time(rate):
# 	return random.expovariate(rate)

# def build_packet_generator(p, l):
# 	cf = [sum(p[:i+1]) for i in range(len(p))]
# 	assert cf[-1] == 1.0, "Not valid probability distribution"

# 	def generate_packet():
# 		x = random.random()
# 		for i, v in enumerate(cf):
# 			if v > x: return l[i]

# 	return generate_packet

# def generate_events(n, rate, generate_packet):
# 	time = 0.0
# 	for _ in range(n):
# 		yield time, generate_packet()
# 		time += next_time(rate)

# n = input()
# rate = input()
# p = map(float, raw_input().split())
# l = map(float, raw_input().split())
# l = dict(enumerate(l))

# for time, packet in generate_events(n, rate, build_packet_generator(p, l)):
# 	print time, packet
