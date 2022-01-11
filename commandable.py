class Commandable():
	def initRadio(self, dev):
		raise Exception("Must implement initRadio(dev)")

	def sendRepeated(self, dev, data):
		for i in range(0, self.repeats):
			dev.RFxmit(data)
			dev.RFxmit(self.pause_frame)

	def send(self, dev, packet):
		raise Exception("Must implement send(dev, packet)")
