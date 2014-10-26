from collections import deque
from itertools import takewhile

from Event import InjectEvent, ErrorEvent

class Events:
    def __init__(self, injectEvents):
    	self.injectEvents, self.sentEvents, self.errorEvents = deque(injectEvents), [], []

    def hasNext(self):
    	return True if self.injectEvents or self.sentEvents else False

    def hasNextInjectNow(self, time):
        return self.injectEvents and self.injectEvents[0].time == time

    def schedule(self, event):
        if isinstance(event, ErrorEvent):
            Events.scheduleEventInList(self.errorEvents, event)
            self.sentEvents = list(takewhile(lambda e: e <= event, self.sentEvents))
        else:
            Events.scheduleEventInList(self.sentEvents, event)

    def scheduleEventInList(eventList, event):
        pos = 0
        while pos < len(eventList) and eventList[pos] < event: pos += 1
        eventList.insert(pos, event)

    def next(self):
        ie = self.injectEvents[0] if self.injectEvents else None
        se = self.sentEvents[0] if self.sentEvents else None
        ee = self.errorEvents[0] if self.errorEvents else None

        event = ie
        if se: event = event if event and event <= se else se
        if ee: event = event if event and event <= ee else ee

        if event:
            if event == ie: return self.injectEvents.popleft()
            if event == se: return self.sentEvents.pop(0)
            return self.errorEvents.pop(0)

    def fromFile(filename):
        with open(filename, 'r') as events:
            return Events(InjectEvent.fromLine(line) for line in events)
