from __future__ import print_function
from database import Packet
import requests
import json
import datetime
import cherrypy
import paho.mqtt.publish as publish
import time
import telepot
from database import Packet



def retrievePosition():
    pos = json.loads(requests.get('https://api.thingspeak.com/channels/252276/feeds/last').content)

    stringa = '{"lat" :' + str(pos['field3']) + ',"long": ' + str(pos['field4']) +'}'

    return stringa



def handle():

    msg = bot.getUpdates()
    lena = len(msg)
    if lena != 0:
        id = msg[lena - 1]['message']['chat']['id']

        if (any(msg[lena-1]['message']['entities'])):
            if(msg[lena-1]['message']['entities'][0]['type']== 'bot_command'):
                if msg[lena-1]['message']['text'] == '/getPosition':
                    try:
                        po = retrievePosition()
                        print (po)
                        pos = json.loads(po)
                        #bot.sendMessage(id,str(pos['lat']) + " and " + str(pos['long']))
                        bot.sendLocation(id,pos['lat'],pos['long'])
                        #print (msg[lena-1]['message']['text'])
                        return

                    except Exception as detail:
                        print (detail)


if __name__ == '__main__':
    bot = telepot.Bot('378511160:AAF8PCogZt5ZtPUp_gaJU2BPMoWnF6-8zuQ')
    while True:
        msg = bot.message_loop(handle())
        time.sleep(5)



