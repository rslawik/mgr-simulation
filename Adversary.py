from Algorithm import Algorithm

class Adversary(Algorithm):
	def __str__(self):
		return "ADV:" + self.__class__.__name__

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
		epsilon = l1 / 2
		if not self.sending:
			if packet == l2:
				self.mode = 'short'
				return l2 - epsilon
			else:
				self.mode = 'long'
				if self.queue[l2]:
					return l2
				else:
					return epsilon

class ESirocco(Adversary):
	mode = None

	def generate(self):
		while True:
			if self.mode == 'short':
				selected = self.model.packets
			elif self.mode == 'long':
				selected = self.model.packets[1:]
			else:
				selected = []
			send = ([packet for packet in selected if self.queue[packet]] or [None])[0]
			yield send

	def scheduleError(self, packet):
		l1 = self.model.packets[0]
		epsilon = l1 / 2
		if packet and not self.sending:
			if packet == l1:
				self.mode = 'long'
				select = ([packet for packet in self.model.packets[1:] if self.queue[packet]] or [None])[0]
				return select or epsilon
			else:
				self.mode = 'short'
				return packet - epsilon
