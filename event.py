class Event:
	def __init__(self, time):
		self.time = time

class InjectEvent(Event):
	def __init__(self, time, packet):
		super(InjectEvent, self).__init__(time)
		self.packet = packet

class SentEvent(Event):
	def __init__(self, time, algorithm):
		super(SentEvent, self).__init__(time)
		self.algorithm = algorithm

class ErrorEvent(Event):
	def __init__(self, time):
		super(ErrorEvent, self).__init__(time)
