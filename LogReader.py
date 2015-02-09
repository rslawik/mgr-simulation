from Event import InjectEvent, SentEvent, ErrorEvent

def parseEntry(entry):
	parts = entry.strip().split()
	return float(parts[0]), parts[1], parts[2:]

class PacketEntry:
	def __init__(self, packet, start, end, successful):
		self.packet = packet
		self.start = start
		self.end = end
		self.successful = successful

class LogReader:
	def __init__(self, filename):
		self.filename = filename
		self.readLog()

	def readLog(self):
		self.injects = []
		self.errors = []
		self.algPackets = []
		self.advPackets = []

		lastScheduledPacket = {}

		def appendPacketEntry(algorithm, time, successful):
			scheduledPacketTime, scheduledPacket = lastScheduledPacket[algorithm]
			packetEntry = PacketEntry(scheduledPacket, scheduledPacketTime, time, successful)
			if algorithm == "ALG":
				self.algPackets.append(packetEntry)
			elif algorithm == "ADV":
				self.advPackets.append(packetEntry)
			del lastScheduledPacket[algorithm]

		with open(self.filename, 'r') as log:
			for entry in log:
				time, event, params = parseEntry(entry)

				if event == 'inject':
					self.injects.append((time, float(params[0])))
				elif event == 'error':
					self.errors.append(time)
					for algorithm in list(lastScheduledPacket.keys()):
						appendPacketEntry(algorithm, time, False)
				elif event == 'schedule':
					lastScheduledPacket[params[0]] = time, float(params[1])
				elif event == 'sent':
					appendPacketEntry(params[0], time, True)
