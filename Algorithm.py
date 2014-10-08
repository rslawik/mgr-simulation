class Algorithm:
	def __init__(self):
		self.sending = None

	def notify(self, event):
		pass

	def schedule(self):
		pass

	def schedulePacket(self, packet):
		pass

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