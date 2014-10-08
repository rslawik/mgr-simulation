from collections import deque
from itertools import takewhile

from Event import ErrorEvent

class Events:
    def __init__(self, injectEvents):
    	self.injectEvents, self.sentEvents = deque(injectEvents), []

    def hasNext(self):
    	return True if self.injectEvents or self.sentEvents else False

    def schedule(self, event):
    	if isinstance(event, ErrorEvent):
    		self.sentEvents = list(takewhile(lambda e: e < event, self.sentEvents))
    	else:
    		self.scheduleSentEvent(event)

    def scheduleSentEvent(self, event):
    	pos = 0
    	while pos < len(self.sentEvents) and self.sentEvents[pos] < event: pos += 1
    	self.sentEvents.insert(pos, event)

    def next(self):
    	if self.injectEvents and self.sentEvents:
    		ie, se = self.injectEvents[0], self.sentEvents[0]
    		return self.injectEvents.popleft() if ie < se else self.sentEvents.pop(0)
    	if self.sentEvents: return self.sentEvents.pop(0)
    	return self.injectEvents.popleft()
