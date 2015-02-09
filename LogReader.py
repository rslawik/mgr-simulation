from Event import InjectEvent, SentEvent, ErrorEvent

def parseEntry(entry):
	parts = entry.strip().split()
	return float(parts[0]), parts[1], parts[2:]

class SendingEntry:
	pass

class LogReader:
	def __init__(self, filename):
		self.filename = filename
		self.readLog()

	def readLog(self):
		# algSent, advSent = 0.0, 0.0
		# self.times, self.ratios = [], []
		# self.sentLog, self.errorLog = [], []
		self.errors = []

		with open(self.filename, 'r') as log:
			for entry in log:
				time, event, params = parseEntry(entry)

				if event == 'inject':
					print('inject')
				elif event == 'error':
					print('error')
				elif event == 'schedule':
					print('schedule')
				elif event == 'sent':
					print('sent')


				# if entry[0] in "#>": continue
				# if "ERROR" in entry:
				# 	time, _ = entry.strip().split()
				# 	time = float(time)
				# 	self.errorLog.append(time)
				# 	continue
				# time, algorithm, packet = entry.strip().split()
				# time, packet = float(time), float(packet)
				# self.sentLog.append((time, algorithm, packet))
				# if algorithm == "ALG":
				# 	algSent += packet
				# else:
				# 	advSent += packet
				# self.times.append(time)
				# self.ratios.append(algSent / advSent if advSent > 0 else 1.0)
