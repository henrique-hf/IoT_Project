from __future__ import print_function
from RegisterPackage import RegisterPackage
from database import Packet
from thingspeak import Truck
import requests
import json
import datetime
import paho.mqtt.publish as publish
import time


if __name__ == '__main__':

    # p  = Packet()
    # pr = p.findLocation('2147483647')
    # print('ciao')

    while True:
        t = Truck()
        print(t.retrieveData('1'))

