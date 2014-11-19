from Algorithm import Algorithm

class Adversary(Algorithm):
	def scheduleError(self, packet):
		pass

class Sirocco_Thm9(Adversary):
	counter = 0

	def generate(self):
		while True:
			send = ([packet for packet in reversed(self.model.packets) if self.queue[packet]] or [None])[0]
			yield send

	def scheduleError(self, packet):
		l1, l2 = self.model.packets
		if packet == l2:
			error = l2-l1 if self.counter % 2 == 0 else l1
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

class SSAdv(Adversary):
	def __init__(self, distribution, log):
		super(SSAdv, self).__init__(distribution, log)
		self.epsilon = 0.00001
		self.shortMode = False

	def schedule(self):
		if self.shortMode:
			for p in self.distribution.packets:
				if self.queue[p] > 0:
					return self.schedulePacket(p)
		else:
			for p in self.distribution.packets[1:]:
				if self.queue[p] > 0:
					return self.schedulePacket(p)

	def scheduleError(self, packet):
		if packet and not self.sending:
			if packet == self.distribution.packets[0]:
				self.shortMode = False
				for p in self.distribution.packets[1:]:
					if self.queue[p] > 0:
						return p
				return self.epsilon
			else:
				self.shortMode = True
				return packet - self.epsilon
