import sys

import PacketGenerator

generatorname, args = sys.argv[1], sys.argv[2:]

generator = getattr(PacketGenerator, generatorname)

for time, packet in generator(*args):
	print(time, packet)
