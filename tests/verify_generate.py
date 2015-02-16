#!/usr/bin/env python3
import sys

if len(sys.argv) != 3:
	sys.exit(1)

from matplotlib import pyplot

from Model import Model
from Events import Events

model, events = Model.fromFile(sys.argv[1]), Events.fromFile(sys.argv[2])
l1, l2 = model.packets

count = dict((p, 0) for p in model.packets)

l1times, l1count, l1theory, l1rate = [], [], [], []
l2times, l2count, l2theory, l2rate = [], [], [], []
ptimes, prate = [], []

events.next()
while events.hasNext():
	event = events.next()
	time, packet = event.time, event.packet
	count[packet] += 1
	if packet == l1:
		l1times.append(time)
		l1count.append(count[packet])
		l1theory.append(model.rate * model.probability(l1) * time)
		l1rate.append(l1count[-1] / l1theory[-1])
	elif packet == l2:
		l2times.append(time)
		l2count.append(count[packet])
		l2theory.append(model.rate * model.probability(l2) * time)
		l2rate.append(l2count[-1] / l2theory[-1])
	ptimes.append(time)
	prate.append(sum(count[p] for p in model.packets) / model.rate / time)

countTotal = sum(count[p] for p in model.packets)
print(count[l1] / countTotal, count[l2] / countTotal)
print(countTotal, model.rate * ptimes[-1], countTotal / model.rate / ptimes[-1])

# l1c, = pyplot.plot(l1times, l1count)
# l1t, = pyplot.plot(l1times, l1theory)

# l2c, = pyplot.plot(l2times, l2count)
# l2t, = pyplot.plot(l2times, l2theory)

# pyplot.legend([l1c, l1t, l2c, l2t], ["$l_1$ count", "$l_1$ theory", "$l_2$ count", "$l_2$ theory"])

# l1r, = pyplot.plot(l1times, l1rate)
# l2r, = pyplot.plot(l2times, l2rate)
lr, = pyplot.plot(l1times, [1] * len(l1times))
lp, = pyplot.plot(ptimes, prate)
#pyplot.legend([l1r, l2r], ["l1 rate", "l2 rate"])
pyplot.ylim(0.95, 1.05)

pyplot.show()
