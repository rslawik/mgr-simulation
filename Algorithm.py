from Event import InjectEvent, SentEvent, ErrorEvent

class LinkError(BaseException):
	pass

class Algorithm:
	def __init__(self, model):
		self.sending, self.model = None, model
		self.queue = dict((packet, 0) for packet in model.packets)
		self.generator = self.generate()

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
			self.error = event

	def schedule(self):
		assert not self.sending
		packet = self.generator.__next__()
		assert packet is None or self.queue[packet]
		if packet: self.queue[packet] -= 1
		self.sending = packet
		return self.sending

class SL(Algorithm):
	def generate(self):
		while True:
			send = ([packet for packet in self.model.packets if self.queue[packet]] or [None])[0]
			yield send

class LL(Algorithm):
	def generate(self):
		while True:
			send = ([packet for packet in reversed(self.model.packets) if self.queue[packet]] or [None])[0]
			yield send

class SLPreamble(Algorithm):
	def generate(self):
		assert len(self.model.packets) == 2
		gamma = int(self.model.packets[-1] / self.model.packets[0])
		while True:
			self.error = None
			try:
				if self.queue[self.model.packets[0]] >= gamma:
					for _ in range(gamma):
						if self.error: raise LinkError()
						yield self.model.packets[0]
				while True:
					if self.error: raise LinkError()
					send = ([packet for packet in reversed(self.model.packets) if self.queue[packet]] or [None])[0]
					yield send
			except LinkError:
				pass

class Greedy(Algorithm):
	def generate(self):
		stack, n = [], len(self.model.packets)
		while True:
			if self.totalLength(n) < self.model.packets[-1]:
				yield None
			else:
				stack.append(n)
				while stack:
					j = stack.pop()
					# print('transmitGroup', j)
					if self.totalLength(j-1) >= self.model.packets[j-1]:
						for _ in range(int(self.model.packets[j-1] / self.model.packets[j-2])):
							stack.append(j-1)
					else:
						yield self.model.packets[j-1]

	def totalLength(self, k):
		return sum(map(lambda l: self.queue[l] * l, self.model.packets[:k]))
