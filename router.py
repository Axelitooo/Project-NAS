import queue
from token_bucket import TokenBucket
from storage import MemoryStorage

class Router:

	def __init__(self, id, state, tokenBucket, neighbours, linkStates, LSDB, bufferSize, sendfunc):
		self.id = id
		self.state = state  # int or boolean
		self.tokenBucket = tokenBucket  # list of tokenBucket
		self.neighbours = neighbours  # dictionary
		self.LSDB = LSDB  # list
		self.lastLSP = 0
		self.buffer = queue.Queue(bufferSize)
		self.sendfunc = sendfunc

	def show_neighbours(self):
		print(self.neighbours)
		
	def update_lsdb(self, link, weight):
		for key in self.LSDB.keys():
			if key == link:
				if weight == -1:
					self.LSDB.remove(link)
					return True
				elif self.LSDB[link] != weight:
					self.LSDB[link] = weight
					return True
				else:
					return False
		self.LSDB[link] = weight
		return True

	def add_neighbour(self, id, weight):
		if id not in self.neighbours.keys():
			self.neighbours[id] = weight
			if update_lsdb(str(self.id)+"->"+str(id), weight):
				self.lastLSP++
		else:
			print("Id already in dictionary")

	def compute_shortest_path(self, router):
		print("computing shortest path")

	def process_packet(self):
		packet = self.buffer.get(False, None)
		if self.state:  # if !down
			if packet.packetType == "ACK":
				# TODO expectedAcks.pop(packet.destination) + queue.cancel(packet.source, seqnum)
				print("ACK received by " + str(self.id) + " from " + str(packet.source))
			elif packet.packetType == "LSP":
				print("LSP received by " + str(self.id) + " from " + str(packet.source))
				ack = Packet(source=packet.destination, destination=packet.source, packetType="ACK", content=None, seqnum=packet.seqnum, size = 1)
				# every LSP packet is ACKed; similarly to TCP behaviour rather than OSPF's one
				# TODO ACK only if update + cancel if updating LSP received
				self.send_packet(ack)
				if self.lastLSP != packet.seqnum: # TODO : else
					if self.lastLSP < packet.seqnum:
						print("Router", self.id, "updating LSDB and FLOODING")
						# update your own LSDB
						content = {}
						for link in packet.content.keys():
							if update_lsdb(link, packet.content[link]):
								content[link] = packet.content[link]
						self.lastLSP = packet.seqnum
						# flood
						# print("Router", self.id, "FLOODING!!")
						for router in self.neighbours.keys():
							if router != packet.source:
								retransmit_packet = Packet(source=self.id, destination=router, packetType="LSP", content=content, seqnum=self.lastLSP, size = 1)
								self.send_packet(retransmit_packet)
								# handle somehow the case when the LSP was lost (ACK not received), related to expectedAcks
					else: # TODO
						print("Router", self.id, "updating", packet.source, "with seqnum", self.lastLSP)
						# the source (other router) has an outdated information, we should update him
						retransmit_packet = Packet(source=self.id, destination=packet.source, packetType="LSP", content=self.LSDB, seqnum=self.lastLSP, size = 1)
						self.send_packet(retransmit_packet)
						# handle somehow the case when the LSP was lost (ACK not received), related to expectedAcks

	def receive_packet(self, packet):
		if self.buffer.full():
			return 0
		else:
			self.buffer.put(packet, False, None)
			return 1

	# sends packet to the scheduler
	def send_packet(self, packet):
		delay = 1_000_000_000
		self.sendfunc(delay, packet.source, packet.destination, packet)

	def send_packet_now(self, packet, now):
		# if the destination is considered to be busy the packed is dropped on the source
		if self.tokenBucket.consume(str(packet.destination), now, packet.size):
			if packet.packetType == "ACK":
				print("ACK sent by " + str(self.id) + " to " + str(packet.destination))
			elif packet.packetType == "LSP":
				# TODO expectedAcks[packet.destination] = TIME  # TO DEFINE
				print("LSP sent by " + str(self.id) + " to " + str(packet.destination))

	def useful_content(self, packet):
		for element in packet.content:
			if element not in self.LSDB:
				return True
		return False

class Packet:
	def __init__(self, source, destination, packetType, content, seqnum, size):
		self.source = source  # router ID
		self.destination = destination  # router ID
		self.packetType = packetType  # packetType is a string, "ACK" or "LSP"
		self.content = content  # content is a dictionary of keys = links ("id1-id2"), values = weights (-1 <=> link down)    {"0->1":1}
		self.seqnum = seqnum
		self.size = size
