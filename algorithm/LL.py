class LL(Algorithm):
	def __init__(self, distribution, log):
		super(LL, self).__init__(distribution, log)

	def schedule(self):
		for packet in reversed(self.distribution.packets):
			if self.queue[packet] > 0:
				return self.schedulePacket(packet)
