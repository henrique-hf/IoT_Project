from __future__ import print_function
from zRegisterPackage import RegisterPackage
from zdatabase import Packet
from zthingspeak import Truck
import requests
import json
import datetime
import paho.mqtt.publish as publish
import time
import zthingspeak
import mqtt
if __name__ == '__main__':

    user_api = '7C2YGM6HF9E63AG2'
    idchannel = mqtt.channelIDretrieve('1')
    api_write = mqtt.channelAPIretrieve(idchannel, user_api)
    t = mqtt.TruckUpdating(api_write, idchannel)
    t.mqttConnection()

