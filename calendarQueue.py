import sched, time
from storage import MemoryStorage
from token_bucket import TokenBucket
from router import Router, Packet


def demi(t):
    return


class CalendarQueue:
    def __init__(self, timefunc, delayfunc):
        self.scheduler = sched.scheduler(timefunc, delayfunc)

    def sendPacket(self, propagation, router_source, router_destination, packet):  # add a sending packet to a neighbour in the calendarQueue
        print(listRouter[router_source].LSDB)
        if packet is None:
            packet = Packet(router_source, router_destination, "LSP", listRouter[router_source].LSDB, str(router_source) + "->" + str(router_destination))
        print("packet send to : ", router_destination)
        listRouter[router_source].send_packet_now(packet, time.time_ns())
        event = self.scheduler.enter(propagation, 1, self.receivePacket, argument=(packet, router_destination))
        if packet.packetType == "LSP":
            packet.add_event(event)

    def triggerPacketIncrement(self, router_source):
        print("Ttiggering increment for router", router_source)
        listRouter[router_source].increment_lsdb_and_flood()

    # def cancelPacket(self, event):
    #     try:
    #         self.scheduler.cancel(event)
    #     except ValueError:
    #         pass

    def receivePacket(self, packet, router_destination):
        res = listRouter[router_destination].receive_packet(packet)
        print("packet received by :", packet.destination, "return code :", res)
        if res == 1:
            listRouter[router_destination].process_packet()


storage_a = MemoryStorage()
storage_b = MemoryStorage()
storage_x = MemoryStorage()
storage_y = MemoryStorage()
storage_z = MemoryStorage()

rate = 10
capacity = 100

bucket_a = TokenBucket(rate, capacity, storage_a)
bucket_b = TokenBucket(rate, capacity, storage_b)
bucket_x = TokenBucket(rate, capacity, storage_x)
bucket_y = TokenBucket(rate, capacity, storage_y)
bucket_z = TokenBucket(rate, capacity, storage_z)

calendarQueue = CalendarQueue(timefunc=time.time_ns, delayfunc=demi)

a = Router(id=0, state=True, tokenBucket=bucket_a, neighbours={}, LSDB={}, bufferSize=10, calendar=calendarQueue,
           linkStates=None)
b = Router(id=1, state=True, tokenBucket=bucket_b, neighbours={}, LSDB={}, bufferSize=10, calendar=calendarQueue,
           linkStates=None)
x = Router(id=2, state=True, tokenBucket=bucket_x, neighbours={}, LSDB={}, bufferSize=10, calendar=calendarQueue,
           linkStates=None)
y = Router(id=3, state=True, tokenBucket=bucket_y, neighbours={}, LSDB={}, bufferSize=10, calendar=calendarQueue,
           linkStates=None)
z = Router(id=4, state=True, tokenBucket=bucket_z, neighbours={}, LSDB={}, bufferSize=10, calendar=calendarQueue,
           linkStates=None)

listRouter = [a, b, x, y, z]
a.add_neighbour(1, 1)
a.add_neighbour(2, 1)
b.add_neighbour(0, 1)
b.add_neighbour(2, 1)
x.add_neighbour(0, 1)
x.add_neighbour(1, 1)

calendarQueue.scheduler.enter(0, 1, calendarQueue.sendPacket, argument=(2_000_000, 0, 2, None))
calendarQueue.scheduler.enter(10_000_000_000, 1, calendarQueue.triggerPacketIncrement, argument=(0,))

calendarQueue.scheduler.run()
