from RegisterPackage import RegisterPackage
from __future__ import print_function
from database import Packet
import requests
import json
import datetime
import paho.mqtt.publish as publish



def testRead():
    test = RegisterPackage()
    test.POST()

    read = test.read()
    check = test.checkData()

    return read, check

#print testRead()
a = testRead()
test = RegisterPackage()
b = test.read();
print a
print b
print b[0]['id']

