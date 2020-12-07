import sched, time
from Token_bucket.storage import MemoryStorage
from .router import Router


s = sched.scheduler(time.time, time.sleep)
"""
a = Router()
b = Router()
x = Router()
y = Router()
z = Router()
"""
listRouter = [a, b, x, y, z]
listBucket = MemoryStorage()

def sendPacket(type, propagation, source, destination): #add a sending packet to a neighbour in the calendarQueue
    print("packet send num: " , num)
    s.enter(propagation,"LSP", receivePacket, argument=(num, type))
    source.sendPacket()

def receivePacket(num, type, destination):
    print("packet received num: " , num)
    destination.receivePacket()

s.enter(5,1, sendPacket, argument=("LSP",2, a.id, b.id))
s.enter(5,2, sendPacket, argument=("LSP",5, a.id, c.id))
#s.enter(10,1, receivePacket, argument=(1))
#s.enter(10,2, receivePacket, argument=(2))

s.run()