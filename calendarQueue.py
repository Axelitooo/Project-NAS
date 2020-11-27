import sched, time
s = sched.scheduler(time.time, time.sleep)

def sendPacket(num, type, propagation):
    print("packet send num: " , num)
    s.enter(propagation,1, receivePacket, argument=(num, type))

def receivePacket(num, type):
    print("packet received num: " , num)

s.enter(5,1, sendPacket, argument=(1, "LSP",2))
s.enter(5,2, sendPacket, argument=(2, "LSP",5))
#s.enter(10,1, receivePacket, argument=(1))
#s.enter(10,2, receivePacket, argument=(2))

s.run()