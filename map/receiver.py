import zmq
import base64
import numpy as np

import json

#This uses zeromq for transferring data. Next 4 lines are for initializing zeromq
context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:8000')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

#this loop just listen and print the message when ever it is received
print("Starting loop...")
while True:
    try:
        message = footage_socket.recv()

        # load the json to a python list and dump it back out as formatted json
        data = json.loads(message)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)
        data_file = 'data2.json'
        with open(data_file, 'w+') as f:
            f.write(s)
            
    except KeyboardInterrupt:
        print("Destroy")
        break
