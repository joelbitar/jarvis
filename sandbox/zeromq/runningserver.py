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
socket.bind("tcp://*:5556")

while True:
    sleep(1)

print("gonna run for eeeva")

socket.send_string("%s %s" % ("testnode", "{}"))

sleep(0.1)
socket.send_string("%s %s" % ("testnode", "{}"))

"""
while True:
    zipcode = 'testnode'
    socket.send_string("%s %s" % (zipcode, input("msg: ")))
    print("sent")
    """
