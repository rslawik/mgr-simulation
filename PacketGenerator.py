
def experiment1(n, p1, p2):
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