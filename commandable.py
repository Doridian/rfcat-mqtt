from abc import ABC, abstractmethod
from time import sleep

dev_class_map = {}

class Commandable(ABC):
	@abstractmethod
	def initRadio(self, dev):
		pass

	@abstractmethod
	def sendInt(self, dev, packet):
		pass

	def __init__(self):
		self.pause_time = 0.01

	def sendRepeated(self, dev, data):
		for i in range(0, self.repeats):
			dev.RFxmit(data)
			sleep(self.pause_time)

	def send(self, dev, packet):
		global dev_class_map
		if dev not in dev_class_map or dev_class_map[dev] != self:
			self.initRadio(dev)
			dev_class_map[dev] = self

		self.sendInt(dev, packet)
