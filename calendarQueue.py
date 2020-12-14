import sched, time
from Token_bucket.storage import MemoryStorage
from Token_bucket.storage_base import StorageBase
from Token_bucket.token_bucket import TokenBucket
from router import Router, Packet

storage = MemoryStorage()
tokenBucket = TokenBucket(10, 100, storage)#rate/s, capacity, storage(list)

def demi(t):
    return

s = sched.scheduler(timefunc = time.time_ns, delayfunc = demi)

a = Router(id = 0, state = True, tokenBucket, neighbors = {}, LSDB= [])
b = Router(id = 1, state = True, tokenBucket, neighbors = {}, LSDB= [])
x = Router(id = 2, state = True, tokenBucket, neighbors = {}, LSDB= [])
y = Router(id = 3, state = True, tokenBucket, neighbors = {}, LSDB= [])
z = Router(id = 4, state = True, tokenBucket, neighbors = {}, LSDB= [])

listRouter = [a, b, x, y, z]
# listBucket = MemoryStorage()

def sendPacket(num, type, propagation, source, destination): #add a sending packet to a neighbour in the calendarQueue
    print("packet send num: ", num )
    s.enter(propagation,"LSP", receivePacket, argument=(num, type))
    source.sendPacket()

def receivePacket(num, type, destination):
    print("packet received num: " , num)
    destination.receivePacket()

s.enter(0,1, sendPacket, argument=(1,"LSP",2000000, a.id, b.id))#, a.id, b.id
s.enter(0,2, sendPacket, argument=(2,"LSP",5000000, a.id, c.id))
#s.enter(10,1, receivePacket, argument=(1))
#s.enter(10,2, receivePacket, argument=(2))

s.run()
