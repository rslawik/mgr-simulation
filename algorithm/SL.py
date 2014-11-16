class SL(Algorithm):
	def __init__(self, distribution, log):
		super(SL, self).__init__(distribution, log)

	def schedule(self):
		for packet in self.distribution.packets:
			if self.queue[packet] > 0:
				return self.schedulePacket(packet)
