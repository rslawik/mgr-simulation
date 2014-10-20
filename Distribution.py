class Distribution:
	def __init__(self, rate, distribution):
		self.rate = rate
		if sum(distribution.values()) != 1.0:
			raise ValueError("{} is not a valid distribution".format(distribution))
		self.distribution = distribution

	def packet(self, packet):
		return self.distribution[packet]

	def packets(self):
		pass
