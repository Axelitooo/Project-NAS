import queue
import sys
from token_bucket import TokenBucket
from storage import MemoryStorage


class Router:

    def __init__(self, id, state, tokenBucket, neighbours, linkStates, LSDB, bufferSize, calendar):
        self.id = id
        self.state = state  # int or boolean
        self.tokenBucket = tokenBucket  # list of tokenBucket
        self.neighbours = neighbours  # dictionary
        self.LSDB = LSDB  # list
        self.buffer = queue.Queue(bufferSize)
        self.calendar = calendar
        self.expectedAcks = {}  # dictionary of packet to be ACKed

    def show_neighbours(self):
        print(self.neighbours)

    def update_lsdb(self, link, value):
        for key in self.LSDB.keys():
            if key == link:
                if value["weight"] == -1:
                    self.LSDB.remove(link)
                    return True
                elif self.LSDB[link]["weight"] != value["weight"]:
                    self.LSDB[link] = value
                    return True
                else:
                    return False
        # if reached here means link not in LSDB
        self.LSDB[link] = value
        return True

    def add_neighbour(self, id, weight):
        if id not in self.neighbours.keys():
            self.neighbours[id] = weight
            self.update_lsdb(str(self.id) + "->" + str(id), {"weight": weight, "seqnum": 1})
        else:
            print("Id already in dictionary")

    def process_packet(self):
        print("processing packet")
        packet = self.buffer.get(False, None)
        if self.state:  # if !down
            if packet.packetType == "ACK":
                # TODO queue.cancel(packet.source, seqnum)
                self.expectedAcks.pop(packet.seqnum)
                print("ACK received by " + str(self.id) + " from " + str(packet.source))
            elif packet.packetType == "LSP":
                print("processing LSP")
                print("LSP received by " + str(self.id) + " from " + str(packet.source))
                ack = Packet(source=packet.destination, destination=packet.source, packetType="ACK",
                             content=None, id=packet.id)
                # every LSP packet is ACKed; similarly to TCP behaviour rather than OSPF's one
                # TODO ACK only if update + cancel if updating LSP received
                self.send_packet(ack)
                for link in packet.content.keys():
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

    def compute_shortest_path(self, start, end, visited=[], distances={}, predecessors={}):
        print("computing shortest path")
        """Find the shortest path between start and end nodes in a graph (LSDB)"""
        # we've found our end node, now find the path to it, and return
        if start == end:
            path = []
            while end is not None:
                path.append(end)
                end = predecessors.get(end, None)
            return distances[start], path[::-1]
        # detect if it's the first time through, set current distance to zero
        if not visited: distances[start] = 0
        # process neighbors as per algorithm, keep track of predecessors
        for neighbor in self.LSDB[start]:
            if neighbor not in visited:
                neighbordist = distances.get(neighbor, sys.maxsize)
                tentativedist = distances[start] + self.LSDB[start][neighbor]
                if tentativedist < neighbordist:
                    distances[neighbor] = tentativedist
                    predecessors[neighbor] = start
        # neighbors processed, now mark the current node as visited
        visited.append(start)
        # finds the closest unvisited node to the start
        unvisiteds = dict((k, distances.get(k, sys.maxsize)) for k in self.LSDB if k not in visited)
        closestnode = min(unvisiteds, key=unvisiteds.get)
        # now we can take the closest node and recurse, making it current
        return self.compute_shortest_path(closestnode, end, visited, distances, predecessors)

    def receive_packet(self, packet):
        if self.buffer.full():
            return 0
        else:
            self.buffer.put(packet, False, None)
            return 1

    # sends packet to the scheduler
    def send_packet(self, packet):
        delay = 1_000_000_000
        self.calendar.sendPacket(delay, packet.source, packet.destination, packet)

    def send_packet_now(self, packet, now):
        # if the destination is considered to be busy the packed is dropped on the source
        if self.tokenBucket.consume(str(packet.destination), now, packet.size):
            if packet.packetType == "ACK":
                print("ACK sent by " + str(self.id) + " to " + str(packet.destination))
            elif packet.packetType == "LSP":
                self.expectedAcks[packet.id] = packet
                # TODO add an event to the calender queue saying "if the router hasn't received an ACK by this time, retransmit the packet"
                print("LSP sent by " + str(self.id) + " to " + str(packet.destination))

    def useful_content(self, packet):
        for element in packet.content.keys():
            if element not in self.LSDB:
                return True
        return False


class Packet:
    def __init__(self, source, destination, packetType, content, id):
        self.source = source  # router ID
        self.destination = destination  # router ID
        self.packetType = packetType  # packetType is a string, "ACK" or "LSP"
        self.content = content  # content is a dictionary of keys = links ("id1-id2"), values = weights
        self.id = id # id of the packet, used for ACK
        self.size = 1  # ACK and LSP occupies the same buffer size
