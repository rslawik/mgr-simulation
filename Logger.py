from Event import SentEvent

class Logger:
	def __init__(self, filename):
		self.filename = filename

	def __enter__(self):
		self.file = open(self.filename, 'w')
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.file.close()

	def log(self, algorithm, event):
		self.file.write("{}\n".format(event))

	def logSent(self, algorithm, event):
		if isinstance(event, SentEvent) and event.algorithm == algorithm:
			self.file.write("{} {}\n".format(event.time, algorithm.sending))
