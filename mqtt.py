from __future__ import print_function
import requests
import json
import datetime
import paho.mqtt.publish as publish
import Adafruit_DHT
import time



def getTHSensorData():
    humidity, temperature = Adafruit_DHT.read_retry(11, 2)  # 11 stands for DHT11 and 2 for pin to read

    data = {'temp': temperature,
            'hum': humidity}

    return data



def channelIDretrieve(truckID):
    channels = requests.get("https://api.thingspeak.com/users/s201586/channels.json").content
    channels_json = json.loads(channels)

    for ch in channels_json["channels"]:
        if ch.get("name") == str(truckID):
            return str(ch.get("id"))


def channelAPIretrieve(channelID, api_key):
    url = 'https://api.thingspeak.com/channels/' + channelID + '?api_key=' + api_key
    print(url)
    x = requests.put(url).content
    xj = json.loads(x)

    for i in xj['api_keys']:
        if i['write_flag'] == True:
            print(i['api_key'])
            return i['api_key']

    print('s')


class TruckUpdating:

    def __init__(self,api_key,channel_id):
        # The Write API Key for the channel
        self.apiKey = api_key
        self.channelID = channel_id


    def mqttConnection(self):

        mqttHost = "mqtt.thingspeak.com"
        tTransport = "websockets"
        tPort = 80
        #mqttHost = '127.0.0.1'


    # Create the topic string
        topic = 'channels/%s/' % self.channelID + 'publish/%s' % self.apiKey
        print (topic)
        temperature = 30
        humidity = 10

        try:
            json_file = open('gps.json').read()
            gps = json.loads(json_file)

        except IOError:
            print ('Errore nell\'apertura del file')


        #while (True):

        for x in gps["trkpt"]:

            data = getTHSensorData()
            temperature = data['temp']
            humidity = data['hum']
            print(" temp =", temperature, "  hum =", humidity)

        # attempt to publish this data to the topic
            try:
                topic = "channels/" + self.channelID + "/publish/" + self.apiKey
                print (topic)
                lat = x['-lat']
                lon = x['-lon']
                tPayload = "field1=" + str(temperature) + "&field2=" + str(humidity) + "&field3=" + str(lat) + "&field4=" + str(lon)
                print (tPayload)
                publish.single(topic, payload=tPayload, hostname=mqttHost)


            except KeyboardInterrupt:
                break

            except Exception as e:
                print("There was an error while publishing the data.",e)

            time.sleep(10)



if __name__ == '__main__':
    user_api = '7C2YGM6HF9E63AG2'

    idchannel = channelIDretrieve(1)
    api_write = channelAPIretrieve(idchannel, user_api)
    t = TruckUpdating(api_write,idchannel)
    t.mqttConnection()
