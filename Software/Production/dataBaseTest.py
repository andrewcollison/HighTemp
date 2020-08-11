import pandas as pd 
import numpy as np 
from datetime import datetime
import time
import paho.mqtt.client as mqtt
from random import seed
from random import random

seed(1)

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/temp1")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    currTime = datetime.datetime.now()
    data = str(msg.payload, 'utf-8')
    logString = str(currTime) + ", " + data + "\n"
    # writeFile(fileName, logString)
    print(logString)




client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect("192.168.0.100", 1883)
# client.subscribe("temp1", qos=1)
client.subscribe([("temp1", 1), ("temp2", 1)])

def main():
    while(1):
        client.loop_start()
        print("Publishing test message")
        # Compile test message
        dateNow = datetime.now()
        sensorID = 101010
        channel = 700 + (round(random(), 4) * 10)
        channe2 = 680 + (round(random(), 4) * 10)
        channe3 = 720 + (round(random(), 4) * 10)
        channe4 = 790 + (round(random(), 4) * 10)
        channe5 = 670 + (round(random(), 4) * 10)

        testString = str(dateNow) + ", " +  str(sensorID) + ", " + str(channel) + ", " + str(channe2)  + ", " + str(channe3)  + ", " +str(channe4) + ", " +str(channe5)
        print(testString)

        client.publish("temp1", testString)
        client.publish("temp1/ch1", channel)
        client.publish("temp1/ch2", channe2)
        client.publish("temp1/ch3", channe3)
        client.publish("temp1/ch4", channe4)
        client.publish("temp1/ch5", channe5)
        client.loop_stop()
        time.sleep(2) # delay

main()