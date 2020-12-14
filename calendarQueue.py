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
# listBucket = MemoryStorage()

def sendPacket(type, propagation, source, destination): #add a sending packet to a neighbour in the calendarQueue
    print("packet send to : ", destination.id )
    s.enter(propagation,"LSP", receivePacket, argument=(type, source))
    #source.sendPacket()

def receivePacket(type, destination):
    print("packet received by : ", destination.id )
    #destination.receivePacket()

s.enter(0,1, sendPacket, argument=("LSP",2000000, a, b))#, a.id, b.id
s.enter(0,2, sendPacket, argument=("LSP",5000000, z, x))
#s.enter(10,1, receivePacket, argument=(1))
#s.enter(10,2, receivePacket, argument=(2))

s.run()
