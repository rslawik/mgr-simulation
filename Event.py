class Event:
	def __init__(self, time):
		self.time = time

	def __lt__(self, other):
		return self.time < other.time

	def __le__(self, other):
		return self < other or self.time == other.time

class InjectEvent(Event):
	def __init__(self, time, packet):
		super(InjectEvent, self).__init__(time)
		self.packet = packet

	def fromLine(line):
		time, packet = line.split()
		return InjectEvent(float(time), float(packet))

	def __str__(self):
		return "{} inject {}".format(self.time, self.packet)

class SentEvent(Event):
	def __init__(self, time, algorithm, packet):
		super(SentEvent, self).__init__(time)
		self.algorithm = algorithm
		self.packet = packet

	def __lt__(self, other):
		if isinstance(other, SentEvent):
			return self.time < other.time or self.time == other.time and self.algorithm < other.algorithm
		return super(SentEvent, self).__lt__(other)

	def __str__(self):
		return "{} sent {} {}".format(self.time, self.algorithm, self.packet)

class ErrorEvent(Event):
	def __init__(self, time):
		super(ErrorEvent, self).__init__(time)

	def __str__(self):
		return "{} error".format(self.time)
