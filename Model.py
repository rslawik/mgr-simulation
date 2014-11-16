class Model:
	"""
	Information about model:
	1. Packet lengths
	2. Parameter lambda (rate)
	3. Length distribution
	"""
	def __init__(self, rate, distribution):
		assert rate is None or sum(distribution.values()) == 1.0, "({}, {}) is not a valid model".format(rate, distribution) 
		self.rate, self.distribution = rate, distribution
		self.packets = sorted(list(distribution.keys()))

	def probability(self, packet):
		return self.distribution[packet]

	def fromFile(fileName):
		with open(fileName, 'r') as description:
			lines = description.readlines()
			packets = list(map(float, lines[0].strip().split()))
			if len(lines) == 1:
				rate, probabilities = None, [None] * len(packets)
			else:
				rate, probabilities = float(lines[1]), map(float, lines[2].strip().split())
			return Model(rate, dict(zip(packets, probabilities)))

	def withPackets(*packets):
		return Model(None, dict((packet, None) for packet in packets))
