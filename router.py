class Router:

    def __init__(self,id , state, tokenBucket, neighbours, LSDB):
        self.__id = id
        self.__state = state                # int or boolean
        self.__tokenBucket = tokenBucket    # list of tockenBucket
        self.__neighbours = neighbours      # dictionnary
        self.__LSDB = LSDB                  # list

    def showNeighbours():
        print(self.__neighbours)

    def addNeighbours(id, weight):
        if id not in self.__neighbours.keys():
            self.__neighbours[id] = weight
        else:
            print("Id already in dictionnary")

    def computeShortestPath(router):
        print("computing shortest path")

    def receivePacket(packet):
        if state != 0: # if !down
            if packet.packetType == "ACK":
                expectedAcks.pop(packet.destination)
                print("ACK received by " + self.id + " from " + packet.source)
            else if packet.packetType == "LSP":
                ack = Packet(source = packet.destination, destination = packet.source, packetType = "ACK")
                sendPacket(ack)
                for router in self.neighbors.keys():
                    if router != packet.source:
                        retransmitPacket = Packet(source = self.id, destination = router, packetType = "LSP", content = packet.content)
                        sendPacket(retransmitPacket)
                print("LSP received by " + self.id + " from " + packet.source)

    def sendPacket(self, packet):
        if self.__tokenBucket.consume(packet.destination, time, packet.size):
            if packet.packetType == "ACK":
                print("ACK sent by " + self.id + " to " + packet.destination)
            else if packet.packetType == "LSP":
                expectedAcks[packet.destination] = TIME # TO DEFINE
                print("LSP sent by " + self.id + " to " + packet.destination)

    def usefulContent(packet):
        for element in packet.content:
            if element not in LSBD:
                return True
        return False

    if __name__ == "__main__":


class Packet(source, destination, packetType, content):
    def __init__(self):
        self.source = source # router ID
        self.destination = destination # router ID
        self.packetType = packetType # packetType is a string, "ACK" or "LSP"
        self.content = content # content is a dictionary of keys = links ("id1-id2"), values = weights
