import sched, time
from storage import MemoryStorage
from token_bucket import TokenBucket
from router import Router, Packet


class SimulatedTime:

    staticTime=0

    def __init__(self, staticTime):
        self.staticTime=staticTime

    def time(self):
        return self.staticTime

    def dummy(self, delay):
        self.staticTime += delay


class CalendarQueue:
    def __init__(self, simu):
        self.scheduler = sched.scheduler(simu.time, simu.dummy)
        self.simu = simu
    def sendPacket(self, propagation, router_source, router_destination, packet):  # add a sending packet to a neighbour in the calendarQueue
        print("TIMESTAMP: " + str(self.simu.time()) + " LSDB source:" + str(router_source) )
        for link in listRouter[router_source].LSDB.keys():
            print(link+str(listRouter[router_source].LSDB[link]))

        if packet is None:
            packet = Packet(router_source, router_destination, "LSP", listRouter[router_source].LSDB, str(router_source) + "->" + str(router_destination))
        # print("packet send to : ", router_destination, " time stamp: ", simu.time())
        self.scheduler.enter(propagation, 1, self.receivePacket, argument=(packet, router_destination))
        listRouter[router_source].send_packet_now(packet, simu.time())

    def scheduleRetransmission(self, delay, retransmission_timer, packet):
        event = self.scheduler.enter(retransmission_timer, 1, self.sendPacket, argument=(delay, packet.source, packet.destination, packet))
        packet.event = event

    def triggerPacketIncrement(self, router_source):
        print("------------------------------------------------------------------------------")
        print("Triggering increment for router", router_source, " time stamp: ", simu.time())
        listRouter[router_source].increment_lsdb_and_flood()

    def cancelPacket(self, event):
        try:
            self.scheduler.cancel(event)
        except ValueError:
            pass

    def receivePacket(self, packet, router_destination):
        res = listRouter[router_destination].receive_packet(packet)
        # print("packet received by :", packet.destination, "return code :", res)
        if res == 1:
            router = listRouter[router_destination]
            process_time = 5
            self.scheduler.enter(process_time, 1, router.process_packet)

if __name__ == "__main__":

    listStorage = []
    listTocken = []
    listRouter = []
    rate = 10
    capacity = 100    
    simu = SimulatedTime(0)
    calendarQueue = CalendarQueue(simu)

    for i in range (10):
        listStorage.append(MemoryStorage())
        listTocken.append(TokenBucket(rate, capacity, listStorage[i]))
        listRouter.append(Router(id=i, x=0, y=0, state=True, tokenBucket=listTocken[i], neighbours={}, LSDB={}, bufferSize=10 ,calendar=calendarQueue, linkStates=None))
        if(i>2):
            listRouter[i].add_neighbour(2, i)
            listRouter[2].add_neighbour(i,i)
    
    listRouter[0].add_neighbour(1,1)
    listRouter[1].add_neighbour(0,1)
    listRouter[1].add_neighbour(2,1)
    listRouter[2].add_neighbour(1,1)

    calendarQueue.scheduler.enter(0, 1, calendarQueue.sendPacket, argument=(2_000, 0, 2, None))
    calendarQueue.scheduler.enter(5_000, 1, calendarQueue.triggerPacketIncrement, argument=(1,))
	# calendarQueue.scheduler.enter(10_000_000_000, 1, lambda: (listRouter[2].down(),
	#                                                           print("Router", 2, "is down!"),
	#                                                           calendarQueue.triggerPacketIncrement(0)))
	# calendarQueue.scheduler.enter(15_000_000_000, 1, lambda: (listRouter[2].up(),
	#                                                           print("Router", 2, "is up!")))
	# calendarQueue.scheduler.enter(20_000_000_000, 1, calendarQueue.triggerPacketIncrement, argument=(2,))
	#
    calendarQueue.scheduler.run()