import zmq
import sys
import time
import datetime
import json

#This uses zeromq for transferring data. Next 3 lines are for initializing zeromq
ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
sock.connect("tcp://127.0.0.1:8000")

print("Starting loop...")
#This loop keep sending data for ever.
while True:
    #data structure, for final version temperature value come from Raspberry, but rest of the data on this project does not change
    data= {}
    data['payload'] = {}
    data['payload']['temperature']= '40.21' 
    data['latitude'] = '64.99307222222222'
    data['height'] = '5'
    data['level'] = '1'
    data['longitude'] = '25.422475'
    data['deviceID'] = 'Raspberry project'
    data['timestamp'] = str(time.time())

    print('%s' % (data))
    #before sending data it is needed to converto to string and then send as string. 
    sock.send_string(json.dumps(data))
    time.sleep( 30 )

sock.close()
ctx.term()