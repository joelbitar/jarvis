#
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

print("gonna run for eeeva")
while True:
    zipcode = randrange(1, 100000)
    zipcode = "44160"
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)

    socket.send_string("%s %i %i" % (zipcode, temperature, relhumidity))
    print("sent")
