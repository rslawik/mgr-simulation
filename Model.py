class Model:
	"""
	Information about model: packet lengths, parameter lambda (rate), length distribution, speedup
	"""
	def __init__(self, rate, distribution, speedup):
		assert rate >= 0.0, "rate has to be >= 0.0"
		assert 1.0 - sum(distribution.values()) <= 0.001, "given distribution is not valid, {} != 1.0".format(sum(distribution.values()))
		assert speedup >= 1.0, "speedup has to be >= 1.0"
		self.rate, self.distribution = rate, distribution
		self.packets = sorted(list(distribution.keys()))
		self.speedup = speedup

	def probability(self, packet):
		return self.distribution[packet]

	def fromFile(fileName):
		with open(fileName, 'r') as modelFile:
			packetsLine, rateLine, distributionLine, speedupLine = modelFile.readlines()
			packets = map(float, packetsLine.strip().split())
			probabilities = map(float, distributionLine.strip().split())
			return Model(float(rateLine), dict(zip(packets, probabilities)), float(speedupLine))

	def withPackets(*packets):
		prob = 1 / len(packets)
		return Model(0.0, dict((packet, prob) for packet in packets), 1.0)
