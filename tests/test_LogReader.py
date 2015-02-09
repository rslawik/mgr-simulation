import unittest

from LogReader import LogReader

class LogReaderTestCase(unittest.TestCase):
	def test_exampleLog(self):
		reader = LogReader('tests/example/test.log')
		self.assertEqual(reader.injects, [(0.0, 123.0), (2.0, 10.0)])
		self.assertEqual(reader.errors, [1.0, 20.0])
		self.assertEqual(len(reader.algPackets), 1)

		algSendingEntry = reader.algPackets[0]
		self.assertEqual(algSendingEntry.packet, 123.0)
		self.assertEqual(algSendingEntry.start, 2.0)
		self.assertEqual(algSendingEntry.end, 20.0)
		self.assertEqual(algSendingEntry.successful, False)

		advSendingEntry = reader.advPackets[0]
		self.assertEqual(advSendingEntry.packet, 10.0)
		self.assertEqual(advSendingEntry.start, 2.0)
		self.assertEqual(advSendingEntry.end, 12.0)
		self.assertEqual(advSendingEntry.successful, True)



if __name__ == '__main__':
	unittest.main()
