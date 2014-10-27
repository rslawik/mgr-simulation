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
		self.counter = 0

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
