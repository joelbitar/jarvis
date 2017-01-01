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

print("gonna run for eeeva")

sleep(1)

socket.send_string("%s %s" % ("testnode", '{}'))

filter_name = input('Filter: ')
while True:
    input_string = input("msg: ") or "test"
    socket.send_string("%s %s" % (filter_name, input_string))
