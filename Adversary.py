from Algorithm import Algorithm

class Adversary(Algorithm):
	def __lt__(self, other):
		return not isinstance(other, Adversary)

	def scheduleError(self, packet):
		pass

class SiroccoThm9(Adversary):
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

class SiroccoThm11(Adversary):
	def generate(self):
		l1 = self.model.packets[0]
		while True:
			yield l1 if self.queue[l1] else None

	def scheduleError(self, packet):
		l1, l2 = self.model.packets
		return l1 / (1 if self.queue[l1] and self.queue[l2] else 2)

class Sirocco(Adversary):
	epsilon = 0.00001
	mode = 'short'

	def generate(self):
		while True:
			if self.mode == 'short':
				# SL
				send = ([packet for packet in self.model.packets if self.queue[packet]] or [None])[0]
				yield send
			else:
				# LL
				send = ([packet for packet in reversed(self.model.packets) if self.queue[packet]] or [None])[0]
				yield send

	def scheduleError(self, packet):
		l1, l2 = self.model.packets
		if not self.sending:
			if packet == l2:
				self.mode = 'short'
				return l2 - self.epsilon
			else:
				self.mode = 'long'
				if self.queue[l2]:
					return l2
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
