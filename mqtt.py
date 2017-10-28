from __future__ import print_function
import requests
import json
import paho.mqtt.publish as publish
import Adafruit_DHT
import time
import datetime
import sys

host = 'http://192.168.1.109:8089'


def getTHSensorData():
    humidity, temperature = Adafruit_DHT.read_retry(11, 2)  # 11 stands for DHT11 and 2 for pin to read

    data = {'temp': temperature,
            'hum': humidity}

    return data


def channelIDretrieve(truckID):
    try:
        trucks = requests.get(host + "/trucks").content
    except:
        print('Server cannot be found. Verify to have the right address and to have a proper connection')
    trucks_json = json.loads(trucks)

    for tr in trucks_json:
        if tr.get("channelName") == truckID:
            return str(tr.get("channelID"))


def channelAPIretrieve(channelID, api_key):
    url = 'https://api.thingspeak.com/channels/%s' % channelID + '?api_key=%s' % api_key
    print(url)
    try:
        x = requests.put(url).content
        xj = json.loads(x)

        for i in xj['api_keys']:
            if i['write_flag'] == True:
                print(i['api_key'])
                return i['api_key']
    except:
        print('Impossible to connect to thingspeak. Check the channelID and the APIkey ')


class TruckUpdating:
    def __init__(self, api_key, channel_id,chanel_name):
        # The Write API Key for the channel
        self.apiKey = api_key
        self.channelID = channel_id
        self.channel_name = chanel_name

    def mqttConnection(self):
        try:
            trucks = json.loads(requests.get(host + '/trucks').content)
            threshold = json.loads(requests.get(host+'/threshold/'+self.channel_name).content)
            print ('thr',threshold)
        except:
            print('Impossible to connect to the server. Check the url and verify that the server is online.')

        for t in trucks:
            if t['channelID'] == self.channelID:
                rate = t['samplingRate']
                break

        mqttHost = "mqtt.thingspeak.com"

        try:
            if self.channel_name == '1':
                json_file = open('gps.json').read()
                gps = json.loads(json_file)

            if self.channel_name == '2':
                json_file = open('gps_lecce_torino.json').read()
                gps = json.loads(json_file)

        except IOError:
            print('Errore nell\'apertura del file')


        for x in gps["trkpt"]:

            data = getTHSensorData()

            temperature = data['temp']
            humidity = data['hum']
            if temperature > int(threshold['temperature']['threshold_max']):
                hasovercome_t = 1
            elif temperature < int(threshold['temperature']['threshold_min']):
                hasovercome_t = -1
            else:
                hasovercome_t = 0
            if humidity > int(threshold['temperature']['threshold_max']):
                hasovercome_h = 1
            elif humidity < int(threshold['temperature']['threshold_min']):
                hasovercome_h = -1
            else:
                hasovercome_h = 0


            print(" temp =", temperature, "  hum =", humidity)

            # attempt to publish this data to the topic
            try:
                topic = "channels/" + self.channelID + "/publish/" + self.apiKey
                print(topic)
                lat = x['-lat']
                lon = x['-lon']
                tPayload = "field1=" + str(temperature) + "&field2=" + str(humidity) + "&field3=" + str(
                    lat) + "&field4=" + str(lon)+"&field5="+str(hasovercome_t)+"&field6="+str(hasovercome_h)
                print(tPayload)
                print('Start pub', datetime.datetime.now())
                publish.single(topic, payload=tPayload, hostname=mqttHost)
                print('End pub', datetime.datetime.now())

            except KeyboardInterrupt:
                break

            except Exception as e:
                print("There was an error while publishing the data.\n", e)

            time.sleep(16)


if __name__ == '__main__':
    try:
        user_api = requests.get(host + '/key').content
        idchannel = channelIDretrieve(sys.argv[1])
        print(idchannel)
        api_write = channelAPIretrieve(idchannel, user_api)
        t = TruckUpdating(api_write, idchannel,sys.argv[1])
        t.mqttConnection()
    except:
        print('Impossible to connect to the server. Check the url and verify that the server is on.')
