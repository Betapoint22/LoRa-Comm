import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX127x
import time
import random

global lora_id
lora_id = random.randint(100000,8452156)
print("LORA ID: {}".format(lora_id))


def trans_setting(msg_data):
	global lora_id
	busId = 0; csId = 0; n=0
	resetPin = 22; irqPin = -1; txenPin = -1; rxenPin = -1
	LoRa = SX127x()
	print("Begin LoRa radio")
	if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin) :
		raise Exception("Something wrong, can't begin LoRa radio")
	print("Seting frequency to 430 Mhz")
	LoRa.setFrequency(430000000)
	print("Set TX power to +17 dBm")
	LoRa.setTxPower(17, LoRa.TX_POWER_PA_BOOST)
	LoRa.setSpreadingFactor(7)# LoRa spreading factor: 7
	LoRa.setBandwidth(125000)# Bandwidth: 125 kHz
	LoRa.setCodeRate(5)
	print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
	LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)                        # Explicit header mode
	LoRa.setPreambleLength(12)                                      # Set preamble length to 12
	LoRa.setPayloadLength(15)                                       # Initialize payloadLength to 15
	LoRa.setCrcEnable(True)
	print("Set syncronize word to 0x34")
	LoRa.setSyncWord(0x34)
	print("\n-- LoRa Transmitter --\n")
	message = msg_data+"\0"
	messageList = list(message)
	for i in range(len(messageList)) : messageList[i] = ord(messageList[i])
	counter = 0
	while n<=0:
		LoRa.beginPacket()
		LoRa.write(messageList, len(messageList))
		LoRa.write([counter], 1)
		LoRa.endPacket()
		print(f"{message}  {counter}")
		LoRa.wait()
		print("Transmit time: {0:0.2f} ms | Data rate: {1:0.2f} byte/s".format(LoRa.transmitTime(), LoRa.dataRate()))
		time.sleep(5)
		counter = (counter + 1) % 256
		n=1

def recev_setting():
	busId = 0; csId = 0 ; n=0
	resetPin = 22; irqPin = -1; txenPin = -1; rxenPin = -1
	LoRa = SX127x()
	print("Begin LoRa radio")
	if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin):
		raise Exception("Something wrong, can't begin LoRa radio")

	print("Set frequency to 430 Mhz")
	LoRa.setFrequency(430000000)

	print("Set RX gain to power saving gain")
	LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING, LoRa.RX_GAIN_AUTO)

	print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
	LoRa.setSpreadingFactor(7)                                      # LoRa spreading factor: 7
	LoRa.setBandwidth(125000)                                       # Bandwidth: 125 kHz
	LoRa.setCodeRate(5)

	print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
	LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)                        # Explicit header mode
	LoRa.setPreambleLength(12)                                      # Set preamble length to 12
	LoRa.setPayloadLength(15)                                       # Initialize payloadLength to 15
	LoRa.setCrcEnable(True)

	print("Set syncronize word to 0x34")
	LoRa.setSyncWord(0x34)
	print("\n-- LoRa Receiver --\n")
	while n<=0:
		message = ""
		LoRa.request()
		LoRa.wait()
		while LoRa.available() > 1 :
			message += chr(LoRa.read())
		counter = LoRa.read()
		print(f"{message}  {counter}")
		print("Packet status: RSSI = {0:0.2f} dBm | SNR = {1:0.2f} dB".format(LoRa.packetRssi(), LoRa.snr()))
		status = LoRa.status()
		if status == LoRa.STATUS_CRC_ERR : print("CRC error")
		elif status == LoRa.STATUS_HEADER_ERR : print("Packet header error")
		n=1
		return message
		time.sleep(5)

trans_setting(str(lora_id)+"/"+"7df8278fffasdop")
data=recev_setting()
print(data)
# rcv = data.split('/')
# print(rcv[0])
# trans_setting(str(rcv[0])+"/"+"Acknowldged")
