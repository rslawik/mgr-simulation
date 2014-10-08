from heapq import heappush, heappop

class Events:
    def __init__(self):
    	self.events = []

    def hasEvents(self):
    	return True if self.events else False

    def schedule(self, event):
    	heappush(self.events, event)
