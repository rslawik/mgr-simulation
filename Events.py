from collections import deque
from itertools import takewhile

from Event import InjectEvent, SentEvent, ErrorEvent, WaitEvent

class Events:
    def __init__(self, injectEvents):
    	self.injectEvents, self.sentEvents, self.errorEvents = deque(injectEvents), [], []

    def hasNext(self):
    	# return True if self.injectEvents or self.sentEvents else False
        return bool(self.injectEvents)

    def hasNextNow(self, time):
        event = self.selectNext()
        return event.time == time if event else False

    def schedule(self, event):
        if isinstance(event, ErrorEvent):
            Events.scheduleEventInList(self.errorEvents, event)
            self.sentEvents = list(takewhile(lambda e: e <= event, self.sentEvents))
        elif isinstance(event, SentEvent):
            if not self.errorEvents or self.errorEvents and event <= self.errorEvents[0]:
                Events.scheduleEventInList(self.sentEvents, event)
        elif isinstance(event, WaitEvent):
            if self.injectEvents:
                error = ErrorEvent(self.injectEvents[0].time)
                self.sentEvents = []
                self.schedule(error)

    def scheduleEventInList(eventList, event):
        pos = 0
        while pos < len(eventList) and eventList[pos] < event: pos += 1
        eventList.insert(pos, event)

    def next(self):
        event = self.selectNext()
        if event:
            if self.injectEvents and event == self.injectEvents[0]: return self.injectEvents.popleft()
            if self.sentEvents and event == self.sentEvents[0]: return self.sentEvents.pop(0)
            if self.errorEvents and event == self.errorEvents[0]: return self.errorEvents.pop(0)

    def selectNext(self):
        event = self.injectEvents[0] if self.injectEvents else None
        if self.sentEvents: event = event if event and event <= self.sentEvents[0] else self.sentEvents[0]
        if self.errorEvents: event = event if event and event <= self.errorEvents[0] else self.errorEvents[0]
        return event

    def fromFile(filename):
        with open(filename, 'r') as events:
            return Events(InjectEvent.fromLine(line) for line in events)
