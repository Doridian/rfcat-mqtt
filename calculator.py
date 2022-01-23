from minka_aire_fan import MinkaAireFan
from binascii import hexlify

class FakeRfCat():
    def __init__(self):
        self.last_data = []
        self.last_data_hex = b""
        self.last_data_raw = b""
        self.last_times = []
        self.setMdmDRate(1000)

    def setFreq(self, freq):
        pass

    def setMdmModulation(self, mod):
        pass

    def setMdmDRate(self, rate):
        self.rate = rate
        self.bitlen_us = round(1_000_000 / rate)

    def makePktFLEN(self, len):
        pass

    def setMdmSyncMode(self, sync):
        pass

    def RFxmit(self, data):
        self.last_data = []
        self.last_times = []
        self.last_data_hex = hexlify(data)
        self.last_data_raw = data
        data = int.from_bytes(data, "big")
        while data > 0:
            bit = data & 1
            self.last_data.append(bit)
            self.last_times.append(self.bitlen_us if bit else -self.bitlen_us)
            data >>= 1

        self.last_times.reverse()
        self.last_data.reverse()

dev = FakeRfCat()

fan = MinkaAireFan()
fan.repeats = 1
fan.send(dev, {
    "command": "light",
    "id": "00101001",
})

print(dev.last_data_hex)
print(dev.last_data_raw)
print(dev.last_data)
print(dev.last_times)

def format_ardu_complex(times):
    res = ""
    last_bit = ""
    last_delay = 0
    for d in times:
        bit = ""
        if d < 0:
            bit = "0"
        elif d > 0:
            bit = "1"
        else:
            continue
        d = abs(d)
        if bit == last_bit:
            last_delay += d
        else:
            if last_bit != "":
                res += "%s%04x" % (last_bit, last_delay)
            last_bit = bit
            last_delay = d

    res += "%s%04x" % (last_bit, last_delay)

    return res

def format_ardu_easy(times, bitlen):
    res = "%04x" % bitlen
    for d in times:
        if d < 0:
            res += "0"
        elif d > 0:
            res += "1"
    return res       

print(format_ardu_complex(dev.last_times))
print(format_ardu_easy(dev.last_times, dev.bitlen_us))
