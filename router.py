<<<<<<< HEAD
import time

class Router:

    def __init__(self,id , state, tokenBucket, neighbors, LSDB):
        self.id = id
        self.state = state                # int or boolean
        self.tokenBucket = tokenBucket    # list of tockenBucket
        self.neighbors = neighbors      # dictionnary
=======
import queue

class Router:

    def __init__(self,id , state, tokenBucket, neighbours, linkStates, LSDB, bufferSize):
        self.id = id
        self.state = state                # int or boolean
        self.tokenBucket = tokenBucket    # list of tockenBucket
        self.neighbours = neighbours      # dictionnary
>>>>>>> 744dbf0b968c49b1b1f69e95f31612f8f5817381
        self.LSDB = LSDB                  # list
        self.lastLSP = {}
        self.buffer = Queue(bufferSize)

    def showNeighbours():
        print(self.neighbours)

    def addNeighbours(id, distance):
        if id not in self.neighbours.keys():
            self.neighbours[id] = distance
        else:
            print("Id already in dictionnary")

    def computeShortestPath(router):
        print("computing shortest path")

    def processPacket():
        packet = self.buffer.get(False, None)
        if state != 0: # if !down
            if packet.packetType == "ACK":
                expectedAcks.pop(packet.destination)
                print("ACK received by " + self.id + " from " + packet.source)
            elif packet.packetType == "LSP":
                ack = Packet(source = packet.destination, destination = packet.source, packetType = "ACK")
                sendPacket(ack)
                for router in self.neighbors.keys():
                    if router != packet.source:
                        if self.lastLSP[packet.source] != packet.seqnum:
                            retransmitPacket = Packet(source = self.id, destination = router, packetType = "LSP", content = packet.content)
                            sendPacket(retransmitPacket)
                            lastLSP[packet.source] = packet.seqnum
                print("LSP received by " + self.id + " from " + packet.source)

    def receivePacket(packet):
        if self.buffer.full():
            return 0
        else:
            self.buffer.put(packet, False, None)
            return 1

        
    def sendPacket(self, packet):
<<<<<<< HEAD
        if self.tokenBucket.consume(packet.destination, time.time_ns(), 1):
=======
        if self.tokenBucket.consume(packet.destination, time, packet.size):
>>>>>>> 744dbf0b968c49b1b1f69e95f31612f8f5817381
            if packet.packetType == "ACK":
                print("ACK sent by " + self.id + " to " + packet.destination)
            elif packet.packetType == "LSP":
                expectedAcks[packet.destination] = time.time_ns() # TO DEFINE ------------------------------------------------------------------------------------------------------------------------------
                print("LSP sent by " + self.id + " to " + packet.destination)

    def usefulContent(packet):
        for element in packet.content:
            if element not in LSBD:
                return True
        return False

    
class Packet(source, destination, seqnum, packetType, content):
    def __init__(self):
        self.source = source # router ID
        self.destination = destination # router ID
        self.seqnum = seqnum
        self.packetType = packetType # packetType is a string, "ACK" or "LSP"
        self.content = content # content is a dictionary of keys = links ("id1-id2"), values = distances
        self.size = 1024