import math

from Algorithm import Algorithm

epsilon = 0.001
wait = -1

class Adversary(Algorithm):
	algorithmType = "ADV"

	def __lt__(self, other):
		return not isinstance(other, Adversary)

	def scheduleError(self, packet):
		pass

class NoErrors(Adversary):
	def generate(self):
		while True:
			for p in self.model.packets:
				if self.queue[p]:
					yield p
					break

	def algorithmSchedules(self, packet):
		pass

	def adversarySchedules(self, packet):
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

class SiroccoI(Adversary):
	mode = None
	sentShort = 0

	def generate(self):
		l1, l2 = self.model.packets
		self.shortInPhase = math.ceil(l2 / l1) - 1
		while True:
			if self.mode == "short":
				packet = l1 if self.queue[l1] else None
				if packet:
					self.sentShort += 1
				else:
					self.sentShort = self.shortInPhase
				yield packet
			else:
				yield ([packet for packet in reversed(self.model.packets) if self.queue[packet]] or [None])[0]

	def algorithmSchedules(self, packet):
		l1, l2 = self.model.packets
		if not self.sending:
			self.sentShort = 0
			if packet == l2:
				self.mode = "short"
				if not self.queue[l1]: return wait
			elif packet == l1:
				self.mode = "long"
				return l2 if self.queue[l2] else wait
			elif packet is None:
				self.mode = "long"

	def adversarySchedules(self, packet):
		l1, l2 = self.model.packets
		if self.sending and self.sentShort == self.shortInPhase:
			# print("% shortInPhase", self.sentShort, self.shortInPhase)
			return l1
		if not self.sending:
			return wait

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
		if packet and not self.sending:
			if packet == l1:
				self.mode = 'long'
				select = ([packet for packet in self.model.packets[1:] if self.queue[packet]] or [None])[0]
				return select or epsilon
			else:
				self.mode = 'short'
				return packet - epsilon
