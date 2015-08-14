#
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq
from time import sleep
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:5556")


print("gonna run for eeeva")

socket.send_string("%s %s" % ("testnode", '{}'))

for i in range(100):
    socket.send_string("%s %s" % ("testnode", '{"t" : "'+ str(i) + '"}'))
    sleep(0.001)


"""
while True:
    zipcode = 'testnode'
    socket.send_string("%s %s" % (zipcode, input("msg: ")))
    print("sent")
    """
