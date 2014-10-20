class Distribution:
	def __init__(self, rate, distribution):
		self.rate = rate
		if sum(distribution.values()) != 1.0:
			raise ValueError("{} is not a valid distribution".format(distribution))
		self.distribution = distribution
		self.packets = list(distribution.keys())
		self.shortestPacket, self.longestPacket = min(self.packets), max(self.packets)

	def probability(self, packet):
		return self.distribution[packet]

	def fromFile(fileName):
		with open(fileName, 'r') as description:
			rate = float(description.readline())
			distribution = {}
			for line in description:
				packet, probability = line.split()
				distribution[float(packet)] = float(probability)
			return Distribution(rate, distribution)
