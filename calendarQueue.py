import sched, time
from storage import MemoryStorage
from token_bucket import TokenBucket
from router import Router, Packet

class CalendarQueue:
    def __init__(self, timefunc, delayfunc):
        self.scheduler = sched.scheduler(timefunc, delayfunc)

def demi(t):
    return

def sendPacket(self, propagation, router_source,
               router_destination, packet):  # add a sending packet to a neighbour in the calendarQueue
    if packet is None:
        packet = Packet(router_source, router_destination, 0, "LSP", None)
    print("packet send to : ", router_destination)
    listRouter[router_source].send_packet_now(packet, time.time_ns())
    s.enter(propagation, 1, receivePacket, argument=(packet, router_destination))


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

a = Router(id=0, state=True, tokenBucket=bucket_a, neighbours={}, LSDB=[], bufferSize=10, sendfunc=sendPacket, linkStates=None)
b = Router(id=1, state=True, tokenBucket=bucket_b, neighbours={0:a}, LSDB=[], bufferSize=10, sendfunc=sendPacket, linkStates=None)
x = Router(id=2, state=True, tokenBucket=bucket_x, neighbours={0:a, 1:b}, LSDB=[], bufferSize=10, sendfunc=sendPacket, linkStates=None)
y = Router(id=3, state=True, tokenBucket=bucket_y, neighbours={}, LSDB=[], bufferSize=10, sendfunc=sendPacket, linkStates=None)
z = Router(id=4, state=True, tokenBucket=bucket_z, neighbours={}, LSDB=[], bufferSize=10, sendfunc=sendPacket, linkStates=None)

listRouter = [a, b, x, y, z]
a.add_neighbour(1, 1)
a.add_neighbour(2, 1)
b.add_neighbour(2, 1)

calendarQueue.scheduler.enter(0, 1, sendPacket, argument=(2000000, 0, 2, None))  # , a.id, b.id
#s.enter(0, 2, sendPacket, argument=(5000000, 2, 3, None))
# s.enter(10,1, receivePacket, argument=(1))
# s.enter(10,2, receivePacket, argument=(2))

calendarQueue.scheduler.run()
