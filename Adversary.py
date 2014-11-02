from Algorithm import Algorithm

class Adversary(Algorithm):
	def __init__(self, distribution, log):
		super(Adversary, self).__init__(distribution, log)

	def scheduleError(self, packet):
		pass

class Experiment1Adv(Adversary):
	def __init__(self, distribution, log):
		super(Experiment1Adv, self).__init__(distribution, log)
		self.counter = 0

	def schedule(self):
		for packet in reversed(self.distribution.packets):
			if self.queue[packet]:
				return self.schedulePacket(packet)

	def scheduleError(self, packet):
		if packet == self.distribution.packets[-1]:
			error = self.distribution.packets[-1]-self.distribution.packets[0] if self.counter % 2 == 0 else self.distribution.packets[0]
			self.counter += 1
			return error

class Experiment3Adv(Adversary):
	def __init__(self, distribution, log):
		super(Experiment3Adv, self).__init__(distribution, log)

	def schedule(self):
		packet = self.distribution.packets[0]
		if self.queue[packet]:
			return self.schedulePacket(packet)

	def scheduleError(self, packet):
		packet1, packet2 = self.distribution.packets[0], self.distribution.packets[-1]
		if self.queue[packet1] and self.queue[packet2]:
			return packet1
		else:
			return packet1 / 2

class SiroccoStochasticAdv(Adversary):
	def __init__(self, distribution, log):
		super(SiroccoStochasticAdv, self).__init__(distribution, log)
		self.epsilon = 0.00001
		self.shortMode = False

	def schedule(self):
		if self.shortMode and self.queue[self.distribution.packets[0]]:
			return self.schedulePacket(self.distribution.packets[0])
		elif self.queue[self.distribution.packets[-1]]:
			return self.schedulePacket(self.distribution.packets[-1])

	def scheduleError(self, packet):
		if not self.sending:
			if packet == self.distribution.packets[-1]:
				self.shortMode = True
				return self.distribution.packets[-1] - self.epsilon
			else:
				self.shortMode = False
				if self.queue[self.distribution.packets[-1]]:
					return self.distribution.packets[-1]
				else:
					return self.epsilon
