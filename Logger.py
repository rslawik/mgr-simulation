from Event import InjectEvent, SentEvent, ErrorEvent

class Logger:
	def __init__(self, algorithm, adversary):
		self.algorithm, self.adversary = algorithm, adversary

	def logEvent(self, event):
		print("# {}".format(event))
		if isinstance(event, SentEvent):
			print("{} {} {}".format(event.time, "ALG" if event.algorithm == self.algorithm else "ADV", event.packet))

	def logAlgorithmSchedule(self, packet, error):
		print("> {} schedules {}; error in {}".format(self.algorithm, packet, error))

	def logAdversarySchedule(self, packet):
		print("> {} schedules {}".format(self.adversary, packet))

class Reader:
	def __init__(self, filename):
		self.filename = filename
		self.readLog()

	def readLog(self):
		algSent, advSent = 0.0, 0.0
		self.times, self.ratios = [], []

		with open(self.filename, 'r') as log:
			for entry in log:
				if entry[0] in "#>": continue
				time, algorithm, packet = entry.strip().split()
				if algorithm == "ALG":
					algSent += float(packet)
				else:
					advSent += float(packet)
				self.times.append(float(time))
				self.ratios.append(algSent / advSent if advSent > 0 else 1.0)
