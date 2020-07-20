import pandas as pd 
import numpy as np 
import datetime
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/temp1")

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print(data)
    client.disconnect()

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    print(str(msg.payload))
       

client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("192.168.0.100", 1883)
client.subscribe("temp1", qos=1)

client.loop_forever()
    
# client = mqtt.Client()
# client.connect("192.168.0.100",1883,60)

# client.on_connect = on_connect
# client.on_message = on_message

# client.loop_forever()