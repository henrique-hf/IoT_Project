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


    p = Packet()
    #p.insertPacketInTruck('111328042017','1')
    t = p.findTruckAssociation('111328042017')
    print (t)
    tr = Truck()
    x = tr.retrieveData(t)

    print (x)


