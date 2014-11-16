class Model:
	def __init__(self, rate, distribution):
		self.rate = rate
		if rate is not None and sum(distribution.values()) != 1.0:
			raise ValueError("{} is not a valid distribution".format(distribution))
		self.distribution = distribution
		self.packets = sorted(list(distribution.keys()))

	def probability(self, packet):
		return self.distribution[packet]

	def fromFile(fileName):
		with open(fileName, 'r') as description:
			lines = description.readlines()
			packets = lines[0].strip().split()
			if len(lines) == 1:
				rate, probabilities = None, [None] * len(packets)
			else:
				rate, probabilities = float(lines[1]), map(float, lines[2].strip().split())
			return Model(rate, dict(zip(map(float, packets), probabilities)))
