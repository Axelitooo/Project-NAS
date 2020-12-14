import sched, time
from storage import MemoryStorage
from storage_base import StorageBase
from token_bucket import TokenBucket
from router import Router, Packet

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

def demi(t):
    return

s = sched.scheduler(timefunc = time.time_ns, delayfunc = demi)

a = Router(id = 0, state = True, tokenBucket = bucket_a, neighbors = {}, LSDB= [], bufferSize = 10)
b = Router(id = 1, state = True, tokenBucket = bucket_b, neighbors = {}, LSDB= [], bufferSize = 10)
x = Router(id = 2, state = True, tokenBucket = bucket_x, neighbors = {}, LSDB= [], bufferSize = 10)
y = Router(id = 3, state = True, tokenBucket = bucket_y, neighbors = {}, LSDB= [], bufferSize = 10)
z = Router(id = 4, state = True, tokenBucket = bucket_z, neighbors = {}, LSDB= [], bufferSize = 10)

listRouter = [a, b, x, y, z]

def sendPacket(propagation, router_source, router_destination): #add a sending packet to a neighbour in the calendarQueue
    print("packet send to : ", router_destination.id )
    packet = Packet(router_source.id, router_destination.id, "LSP", "")
    s.enter(propagation,1, receivePacket, argument=(packet, router_destination))
    router_source.sendPacket(packet)

def receivePacket(packet, router_destination):
    print("packet received by : ", packet.destination)
    router_destination.receivePacket(packet)

s.enter(0,1, sendPacket, argument=(2000000, a, b))#, a.id, b.id
s.enter(0,2, sendPacket, argument=(5000000, x, y))
#s.enter(10,1, receivePacket, argument=(1))
#s.enter(10,2, receivePacket, argument=(2))

s.run()
