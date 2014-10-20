class Distribution:
	def __init__(self, rate, distribution):
		self.rate = rate
		if sum(distribution.values()) != 1.0:
			raise ValueError("{} is not a valid distribution".format(distribution))
		self.distribution = distribution
		self.packets = list(distribution.keys())

	def probability(self, packet):
		return self.distribution[packet]
