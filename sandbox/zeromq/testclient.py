
#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server…")
socket.connect("tcp://localhost:5556")

filter_name = input('Filter: ') 
socket.setsockopt_string(zmq.SUBSCRIBE, filter_name)

# Process 5 updates
while True:
    string = socket.recv_string()
    print('received', string)
