from Algorithm import Algorithm

class Adversary(Algorithm):
	def __init__(self, distribution, log):
		super(Adversary, self).__init__(distribution, log)

	def scheduleError(self, packet):
		pass

class Experiment1Adversary(Adversary):
	def __init__(self, distribution, log):
		super(Experiment1Adversary, self).__init__(distribution, log)
		self.counter = 0

	def schedule(self):
		for packet in reversed(self.distribution.packets):
			if self.queue[packet] > 0:
				return self.schedulePacket(packet)

	def scheduleError(self, packet):
		if packet == self.distribution.packets[-1]:
			error = self.distribution.packets[-1]-self.distribution.packets[0] if self.counter % 2 == 0 else self.distribution.packets[0]
			self.counter += 1
			return error
