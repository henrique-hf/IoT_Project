from __future__ import print_function
import requests
import json
import time
import telepot
from database import Packet
from thingspeak import Truck


def retrievePosition(id):
    p = Packet()
    truckid = Packet.findTruckAssociation(p,id)
    if truckid == 0:
        return None
    channel = Truck.channelIDretrieve(Truck(),truckid)
    url = 'https://api.thingspeak.com/channels/'+str(channel)+'/feeds/last'
    pos = json.loads(requests.get(url).content)
    stringa = '{"lat" :' + str(pos['field3']) + ',"long": ' + str(pos['field4']) +'}'


    return stringa


def internal(msg):
    return msg['text']


def on_message(msg):
    print ('Son passato')

    lena = len(msg)
    if lena != 0:
        id = msg['chat']['id']

        try:
            any(msg['entities'])

        except:
            bot.sendMessage(id,'You should send me a command')
            bot.sendMessage(id,msg['text'])
            return

        if(msg['entities'][0]['type']== 'bot_command'):

            if msg['text'] == '/getposition':

                bot.sendMessage(id,"Enter yuor pack code:")
                time.sleep(10)
                updates = bot.getUpdates()

                packet = (updates[len(updates)-1]['message']['text'])

                try:
                    po = retrievePosition(str(packet))

                except Exception as detail:
                    bot.sendMessage("Error in accessing the database")
                    return

                if po is not None:
                    pos = json.loads(po)
                    bot.sendLocation(id, pos['lat'], pos['long'])
                    return

                else:
                    bot.sendMessage(id,'Your packet is not in the system')

            elif msg['text'] == "/gettemperature":
                return

            elif msg['text'] == "/gethumidity":
                return

            elif msg['text'] == "/getall":
                return

        else:
            return


if __name__ == '__main__':
    bot = telepot.Bot('378511160:AAF8PCogZt5ZtPUp_gaJU2BPMoWnF6-8zuQ')
    bot.message_loop({'chat':on_message},relax=60,run_forever=True)

