from Event import InjectEvent, SentEvent, ErrorEvent

class Algorithm:
	def __init__(self, distribution):
		self.sending, self.distribution = None, distribution
		self.queue = dict((packet, 0) for packet in distribution.packets)

	def __str__(self):
		return self.__class__.__name__

	def notify(self, event):
		if isinstance(event, InjectEvent):
			self.queue[event.packet] += 1
		elif isinstance(event, SentEvent) and event.algorithm == self:
			self.sending = None
		elif isinstance(event, ErrorEvent):
			if self.sending: self.queue[self.sending] += 1
			self.sending = None

	def schedule(self):
		pass

	def schedulePacket(self, packet):
		assert not self.sending
		assert self.queue[packet] > 0
		self.sending = packet
		self.queue[packet] -= 1
		return self.sending

class SL(Algorithm):
	def schedule(self):
		for packet in self.distribution.packets:
			if self.queue[packet] > 0:
				return self.schedulePacket(packet)

class LL(Algorithm):
	def __init__(self, distribution, log):
		super(LL, self).__init__(distribution, log)

	def schedule(self):
		for packet in reversed(self.distribution.packets):
			if self.queue[packet] > 0:
				return self.schedulePacket(packet)

class SLPreamble(Algorithm):
	def __init__(self, distribution, log):
		super(SLPreamble, self).__init__(distribution, log)
		self.preamble, self.gamma = [], int(self.distribution.packets[-1] / self.distribution.packets[0])

	def schedule(self):
		if not self.preamble and self.queue[self.distribution.packets[0]] >= self.gamma:
			self.preamble = [self.distribution.packets[0]] * self.gamma
		elif self.preamble:
			nextPacket = self.preamble.pop()
			return self.schedulePacket(nextPacket)
		elif self.queue[self.distribution.packets[-1]]:
			return self.schedulePacket(self.distribution.packets[-1])

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
