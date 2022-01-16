from abc import ABC, abstractmethod

dev_class_map = {}

class Commandable(ABC):
	@abstractmethod
	def initRadio(self, dev):
		pass

	@abstractmethod
	def sendInt(self, dev, packet):
		pass

	def sendRepeated(self, dev, data):
		res = b''
		for i in range(0, self.repeats):
			res += data + self.pause_frame
		dev.RFxmit(res)

	def send(self, dev, packet):
		global dev_class_map
		if dev not in dev_class_map or dev_class_map[dev] != self:
			self.initRadio(dev)
			dev_class_map[dev] = self

		self.sendInt(dev, packet)
