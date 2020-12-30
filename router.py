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
        self.lastLSP = -1
        self.buffer = queue.Queue(bufferSize)
        self.sendfunc = sendfunc

    def show_neighbours(self):
        print(self.neighbours)

    def add_neighbour(self, id, weight):
        if id not in self.neighbours.keys():
            self.neighbours[id] = weight
        else:
            print("Id already in dictionary")

    def compute_shortest_path(self, router):
        print("computing shortest path")

    def process_packet(self):
        print("processing packet")
        packet = self.buffer.get(False, None)
        if self.state:  # if !down
            if packet.packetType == "ACK":
                # TODO expectedAcks.pop(packet.destination) + queue.cancel(packet.source, seqnum)
                print("ACK received by " + str(self.id) + " from " + str(packet.source))
            elif packet.packetType == "LSP":
                print("processing LSP")
                print("LSP received by " + str(self.id) + " from " + str(packet.source))
                ack = Packet(source=packet.destination, destination=packet.source, packetType="ACK", seqnum=packet.seqnum, content=None)
                # every LSP packet is ACKed; similarly to TCP behaviour rather than OSPF's one
                # TODO ACK only if update + cancel if updating LSP received
                self.send_packet(ack)
                if self.lastLSP != packet.seqnum:
                    if self.lastLSP < packet.seqnum:
                        print("Router", self.id, "updating LSDB")
                        # update your own LSDB
                        self.LSDB = packet.content
                        self.lastLSP = packet.seqnum
                        # flood
                        print("Router", self.id, "FLOODING!!")
                        for router in self.neighbours.keys():
                            if router != packet.source:
                                retransmit_packet = Packet(source=self.id, destination=router, packetType="LSP",
                                                           content=self.LSDB, seqnum=self.lastLSP)
                                self.send_packet(retransmit_packet)
                                # handle somehow the case when the LSP was lost (ACK not received), related to expectedAcks
                    else:
                        print("Router", self.id, "updating", packet.source, "with seqnum", self.lastLSP)
                        # the source (other router) has an outdated information, we should update him
                        retransmit_packet = Packet(source=self.id, destination=packet.source, packetType="LSP",
                                                   content=self.LSDB, seqnum=self.lastLSP)
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
    def __init__(self, source, destination, seqnum, packetType, content):
        self.source = source  # router ID
        self.destination = destination  # router ID
        self.seqnum = seqnum
        self.packetType = packetType  # packetType is a string, "ACK" or "LSP"
        self.content = content  # content is a dictionary of keys = links ("id1-id2"), values = weights
        self.size = 1  # ACK and LSP occupies the same buffer size
