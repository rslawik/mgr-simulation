from Event import InjectEvent, SentEvent, ErrorEvent

class Algorithm:
	def __init__(self, distribution, log):
		self.sending, self.distribution = None, distribution
		self.queue = dict((packet, 0) for packet in distribution.packets)
		self.log = log

	def notify(self, event):
		self.log(self, event)
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

class SLAlgorithm(Algorithm):
	def __init__(self, distribution, log):
		super(SLAlgorithm, self).__init__(distribution, log)

	def schedule(self):
		for packet in self.distribution.packets:
			if self.queue[packet] > 0:
				return self.schedulePacket(packet)

class LLAlgorithm(Algorithm):
	def __init__(self, distribution, log):
		super(LLAlgorithm, self).__init__(distribution, log)

	def schedule(self):
		for packet in reversed(self.distribution.packets):
			if self.queue[packet] > 0:
				return self.schedulePacket(packet)

# class SLPreamble(Algorithm):
# 	preamble = []

# 	def __init__(self, packet_lengths, gamma):
# 		# call parent constructor
# 		self.gamma = gamma

# 	def schedule(self):
# 		print 'SLPreamble schedule'
# 		if not self.preamble and self.package_count(self.l_min) >= self.gamma:
# 			self.preamble = [self.l_min] * self.gamma
# 			for _ in range(self.gamma): del self.queue[self.queue.index(self.l_min)]
# 		elif self.preamble:
# 			self.last_package = self.preamble.pop()
# 		elif self.l_max in self.queue:
# 			self.last_package = self.l_max
# 			del self.queue[self.queue.index(self.last_package)]
# 		return self.last_package

# 	def notify(self, status):
# 		Algorithm.notify(self, status)