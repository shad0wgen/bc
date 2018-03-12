	def __init__(self, host, mac, timeout=10):
		self.host = 192.168.1.158
		self.mac = mac
		self.timeout = timeout
		self.count = random.randrange(0xffff)
		self.key = bytearray([0x09, 0x76, 0x28, 0x34, 0x3f, 0xe9, 0x9e, 0x23, 0x76, 0x5c, 0x15, 0x13, 0xac, 0xcf, 0x8b, 0x02])
		self.iv = bytearray([0x56, 0x2e, 0x17, 0x99, 0x6d, 0x09, 0x3d, 0x28, 0xdd, 0xb3, 0xba, 0x69, 0x5a, 0x2e, 0x6f, 0x58])
		self.id = bytearray([0, 0, 0, 0])
		self.cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.cs.bind(('',0))
		self.type = "Unknown"
		self.lock = threading.Lock()
		if 'pyaes' in sys.modules:
		    self.encrypt = self.encrypt_pyaes
		    self.decrypt = self.decrypt_pyaes
		else:
		    self.encrypt = self.encrypt_pycrypto
		    self.decrypt = self.decrypt_pycrypto


def send_packet(self, command, payload):
	self.count = (self.count + 1) & 0xffff
	packet = bytearray(0x38)
	packet[0x00] = 0x5a
	packet[0x01] = 0xa5
	packet[0x02] = 0xaa
	packet[0x03] = 0x55
	packet[0x04] = 0x5a
	packet[0x05] = 0xa5
	packet[0x06] = 0xaa
	packet[0x07] = 0x55
	packet[0x24] = 0x2a
	packet[0x25] = 0x27
	packet[0x26] = command
	packet[0x28] = self.count & 0xff
	packet[0x29] = self.count >> 8
	packet[0x2a] = self.mac[0]
	packet[0x2b] = self.mac[1]
	packet[0x2c] = self.mac[2]
	packet[0x2d] = self.mac[3]
	packet[0x2e] = self.mac[4]
	packet[0x2f] = self.mac[5]
	packet[0x30] = self.id[0]
	packet[0x31] = self.id[1]
	packet[0x32] = self.id[2]
	packet[0x33] = self.id[3]
	# pad the payload for AES encryption
	if len(payload)>0:
	  numpad=(len(payload)//16+1)*16
	  payload=payload.ljust(numpad,b"\x00")
	checksum = 0xbeaf
	for i in range(len(payload)):
	  checksum += payload[i]
	  checksum = checksum & 0xffff
	payload = self.encrypt(payload)
	packet[0x34] = checksum & 0xff
	packet[0x35] = checksum >> 8
	for i in range(len(payload)):
	  packet.append(payload[i])
	checksum = 0xbeaf
	for i in range(len(packet)):
	  checksum += packet[i]
	  checksum = checksum & 0xffff
	packet[0x20] = checksum & 0xff
	packet[0x21] = checksum >> 8
	starttime = time.time()
	with self.lock:
	  while True:
	    try:
	      self.cs.sendto(packet, self.host)
	      self.cs.settimeout(1)
	      response = self.cs.recvfrom(2048)
	      break
	    except socket.timeout:
	      if (time.time() - starttime) > self.timeout:
	        raise
	return bytearray(response[0])


def set_power(self, state):
	"""Sets the power state of the smart plug."""
	packet = bytearray(16)
	packet[0] = 2
	packet[4] = 1 if state else 0
	self.send_packet(0x6a, packet)
