from Event import InjectEvent, SentEvent, ErrorEvent

class Algorithm:
	def __init__(self, distribution):
		self.sending, self.distribution = None, distribution
		self.queue = dict((packet, 0) for packet in distribution.packets)

	def notify(self, event):
		if isinstance(event, InjectEvent):
			self.queue[event.packet] += 1
		elif isinstance(event, SentEvent):
			print('sent')
			self.sending = None
		elif isinstance(event, ErrorEvent):
			self.notify(InjectEvent(event.time, self.sending))
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
	def __init__(self, distribution):
		super(SLAlgorithm, self).__init__(distribution)

	def schedule(self):
		for packet in self.distribution.packets:
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