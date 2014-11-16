class Greedy(Algorithm):
	def __init__(self, distribution, log):
		super(Greedy, self).__init__(distribution, log)
		self.greedy = self.greedyGenerator()

	def totalLength(self, k):
		return sum(map(lambda l: self.queue[l] * l, self.distribution.packets[:k]))

	def greedyGenerator(self):
		stack, n = [], len(self.distribution.packets)
		while True:
			if self.totalLength(n) < self.distribution.packets[-1]:
				yield None
			else:
				stack.append(n)
				while stack:
					j = stack.pop()
					# print('transmitGroup', j)
					if self.totalLength(j-1) >= self.distribution.packets[j-1]:
						for _ in range(int(self.distribution.packets[j-1] / self.distribution.packets[j-2])):
							stack.append(j-1)
					else:
						yield self.distribution.packets[j-1]

	def schedule(self):
		packet = self.greedy.__next__()
		if packet:
			return self.schedulePacket(packet)
