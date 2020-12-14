import sched, time
from Token_bucket.storage import MemoryStorage
from Token_bucket.storage_base import StorageBase
from Token_bucket.token_bucket import TokenBucket
from router import Router, Packet

storage_a = MemoryStorage()
storage_b = MemoryStorage()
storage_x = MemoryStorage()
storage_y = MemoryStorage()
storage_z = MemoryStorage()

def demi(t):
    return

s = sched.scheduler(timefunc = time.time_ns, delayfunc = demi)

a = Router(id = 0, state = True, storage = storage_a, neighbors = {}, LSDB= [])
b = Router(id = 1, state = True, storage = storage_b, neighbors = {}, LSDB= [])
x = Router(id = 2, state = True, storage = storage_x, neighbors = {}, LSDB= [])
y = Router(id = 3, state = True, storage = storage_y, neighbors = {}, LSDB= [])
z = Router(id = 4, state = True, storage = storage_z, neighbors = {}, LSDB= [])

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
