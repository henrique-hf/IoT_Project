import paho
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import requests
import json
import time


api_key = '1F5B7VCHIUYER0CK'
host = 'mqtt.thingspeak.com'

def mqttpub(temp,hum,channel):
    global api_key

    message = "field1=" + str(temp) + "&field2=" + str(hum)
    topic = "channels/"+channel+"/publish/"+api_key

    try:
        publish.single(topic=topic,payload=message,hostname=host)

    except Exception:
        print (Exception.message)

    return


def channelIDretrieve(self, truckID):
    channels = requests.get("https://api.thingspeak.com/users/s201586/channels.json").content
    channels_json = json.loads(channels)

    for ch in channels_json["channels"]:
        if ch.get("name") == str(truckID):
            return str(ch.get("id"))



if __name__ == '__main__':

    temp = 0
    hum = 0

    while True:
        temp += 5
        hum += 10
        mqttpub(temp,hum,'252276')
        time.sleep(2)

