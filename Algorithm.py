from Event import InjectEvent, SentEvent, ErrorEvent

class LinkError(BaseException):
	pass

class Algorithm:
	def __init__(self, model):
		self.sending, self.model = None, model
		self.queue = dict((packet, 0) for packet in model.packets)
		self.generator = self.generate()

	def __lt__(self, other):
		return False

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

class CSLPreamble(Algorithm):
	def generate(self):
		assert len(self.model.packets) == 2
		l1 = self.model.packets[0]
		p = self.model.probability(l1)
		# there should be smarter way to do it
		return self.generate_SL() if self.model.rate * l1 * p > 0.5 else self.generate_SLPreamble()

	def generate_SL(self):
		while True:
			send = ([packet for packet in self.model.packets if self.queue[packet]] or [None])[0]
			yield send

	def generate_SLPreamble(self):
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

class Prudent(Algorithm):
	def generate(self):
		lk = self.model.packets[-1]
		while True:
			self.error = None
			try:
				toSend = self.selectToSend(lk, lk)
				if not toSend:
					yield None
				else:
					i = toSend[0]
					if i < lk:
						li1 = self.nextLonger(i)
						for _ in range(int(li1/i)):
							yield i
							if self.error: raise LinkError()
						lsent = li1
						while lsent < lk:
							j = self.selectToSend(lk - lsent, lsent)
							lj1 = self.nextLonger(j)
							for _ in range(int(lj1/j)):
								yield j
								if self.error: raise LinkError()
							lsent = lsent + lj1
					while True:
						# LL
						send = ([packet for packet in reversed(self.model.packets) if self.queue[packet]] or [None])[0]
						yield send
						if self.error: raise LinkError()
			except LinkError:
				pass

	def selectToSend(self, lk, longest):
		return [l for l in self.model.packets if l * self.queue[l] >= lk and l <= longest]

	def nextLonger(self, li):
		return self.model.packets[self.model.packets.index(li)+1]

class ESLPreamble(Algorithm):
	def generate(self):
		assert len(self.model.packets) == 3
		l1, l2, l3 = self.model.packets
		# gamma = int(self.model.packets[-1] / self.model.packets[0])
		while True:
			self.error = None
			try:
				# enough l1 to send l2
				if self.queue[l1] * l1 >= l2:
					for _ in range(int(l2/l1)):
						yield l1
						if self.error: raise LinkError()
				# enough l1 and l2 to send l3
				if self.queue[l1] * l1 + self.queue[l2] * l2 >= l3:
					lsent = 0
					while lsent < l3:
						if self.queue[l1]: yield l1
						else: self.queue[l2]: yield l2
						if self.error: raise LinkError()
				# LL
				while True:
					if self.error: raise LinkError()
					send = ([packet for packet in reversed(self.model.packets) if self.queue[packet]] or [None])[0]
					yield send
			except LinkError:
				pass
