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
    #here
    try:
        trucks = requests.get("http://192.168.1.102:8089/trucks").content
        print (trucks)
    except:
        print ('Server cannot be found. Verify to have the right address and to have a proper connection')
    trucks_json = json.loads(trucks)

    for tr in trucks_json["channels"]:
        if tr.get("channelName") == truckID:
            return str(tr.get("channelID"))


def channelAPIretrieve(channelID, api_key):

    url = 'https://api.thingspeak.com/channels/%s' % channelID + '?api_key=%s' % api_key
    print(url)
    x = requests.put(url).content
    xj = json.loads(x)

    for i in xj['api_keys']:
        if i['write_flag'] == True:
            print(i['api_key'])
            return i['api_key']




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
            #temperature = 22
            #humidity = 33
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
                print("There was an error while publishing the data.\n",e)

            time.sleep(5)



if __name__ == '__main__':
    #here
    user_api = requests.get('http://192.168.1.102/key').content
    idchannel = channelIDretrieve('1')
    api_write = channelAPIretrieve(idchannel, user_api)
    t = TruckUpdating(api_write,idchannel)
    t.mqttConnection()