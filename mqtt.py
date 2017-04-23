from __future__ import print_function
from database import Packet
import requests
import json
import datetime
import paho.mqtt.publish as publish
import time

class TruckUpdating:

    def __init__(self):
        # The Write API Key for the channel
        # Replace this with your Write API key
        self.apiKey = "VCQKP9ZXDFINTNWO"


    def mqttConnection(self,channelID):
        #  MQTT Connection Methods

        # Set useUnsecuredTCP to True to use the default MQTT port of 1883
        # This type of unsecured MQTT connection uses the least amount of system resources.
        useUnsecuredTCP = False

        # Set useUnsecuredWebSockets to True to use MQTT over an unsecured websocket on port 80.
        # Try this if port 1883 is blocked on your network.
        useUnsecuredWebsockets = False

        # Set useSSLWebsockets to True to use MQTT over a secure websocket on port 443.
        # This type of connection will use slightly more system resources, but the connection
        # will be secured by SSL.
        useSSLWebsockets = True

        ###   End of user configuration   ###

        # The Hostname of the ThinSpeak MQTT service
        mqttHost = "mqtt.thingspeak.com"

    # Set up the connection parameters based on the connection type
        if useUnsecuredTCP:
            tTransport = "tcp"
            tPort = 1883
            tTLS = None

        if useUnsecuredWebsockets:
            tTransport = "websockets"
            tPort = 80
            tTLS = None

        if useSSLWebsockets:
            import ssl

            tTransport = "websockets"
            tTLS = {'ca_certs': "/etc/ssl/certs/ca-certificates.crt", 'tls_version': ssl.PROTOCOL_TLSv1}
            tPort = 443

    # Create the topic string
        topic = "channels/" + channelID + "/publish/" + self.apiKey
        print (topic)

    # Run a loop which calculates the system performance every
    #   20 seconds and published that to a ThingSpeak channel
    #   using MQTT.

        temperature = 30
        humidity = 10

        try:
           json_file =  open('gps.json').read()
           gps = json.loads(json_file)

        except:
            print ('Errore nell\'apertura del file')


        #while (True):

        for x in gps["trkpt"]:

        # get the system performance data
            temperature = temperature + 0.5
            humidity = humidity + 0.35
            print(" temp =", temperature, "  hum =", humidity)

        # build the payload string
            tPayload = "field1=" + str(temperature) +"&field2=" + str(humidity)+"&field3=" + str(x["-lat"]) + "&field4="+str(x["-lon"])

            print (tPayload)
        # attempt to publish this data to the topic
            try:
                publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)

            except (KeyboardInterrupt):
                break

            except:
                print("There was an error while publishing the data.")

            time.sleep(20)

    def channelIDretrieve(self,truckID):
        channels = requests.get("https://api.thingspeak.com/users/s201586/channels.json").content
        channels_json = json.loads(channels)

        for ch in channels_json["channels"]:
            if ch.get("name") == str(truckID):
                return str(ch.get("id"))


if __name__ == '__main__':
    t = TruckUpdating()
    idchannel = t.channelIDretrieve(1)
    print (idchannel)
    t.mqttConnection(idchannel)