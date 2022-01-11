from commandable import Commandable
from rflib import MOD_ASK_OOK

_COMMANDS = {
	'off':     0b10100,
	'low':     0b00100,
	'medium':  0b01000,
	'high':    0b10000,
	'light_1': 0b01010,
	'light_2': 0b10010,
}
_COMMANDS['light'] = _COMMANDS['light_1']

# IDX = 8, COMMAND = 3, POST = 2
_COMMAND_LEN = 8 + 3 + 2
_PACKET_LEN = 5 # bytes

class MinkaAireFan(Commandable):
	def __init__(self):
		self.repeats = 5
		self.pause_frame = b"\0" * _PACKET_LEN

	def initRadio(self, dev):
		dev.setFreq(304_200_000)
		dev.setMdmModulation(MOD_ASK_OOK)
		dev.setMdmDRate(2400)
		dev.makePktFLEN(_PACKET_LEN)
		dev.setMdmSyncMode(0)

	def send(self, dev, packet):
		command = _COMMANDS[packet["command"]]
		id = int(packet["id"], 2)
		data = (id << 5) | command
		rawData = 0
		for i in range(0, _COMMAND_LEN):
			rawData |= (0b100 | ((data >> i) & 1)) << (i * 3)
		rawData <<= 1
		rawDataB = rawData.to_bytes(5, "big")
		self.sendRepeated(dev, rawDataB)