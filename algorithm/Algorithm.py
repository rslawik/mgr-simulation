from Event import InjectEvent, SentEvent, ErrorEvent

class Algorithm:
	def __init__(self, distribution, log):
		self.sending, self.distribution = None, distribution
		self.queue = dict((packet, 0) for packet in distribution.packets)
		self.log = log

	def __str__(self):
		return self.__class__.__name__

	def notify(self, event):
		self.log(self, event)
		if isinstance(event, InjectEvent):
			self.queue[event.packet] += 1
		elif isinstance(event, SentEvent) and event.algorithm == self:
			self.sending = None
		elif isinstance(event, ErrorEvent):
			if self.sending: self.queue[self.sending] += 1
			self.sending = None

	def schedule(self):
		pass

	def schedulePacket(self, packet):
		assert not self.sending
		assert self.queue[packet] > 0
		self.sending = packet
		self.queue[packet] -= 1
		return self.sending
