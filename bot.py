from __future__ import print_function
import requests
import json
import time
import telepot
from database import Packet
from thingspeak import Truck

# 171602042017

last_processed = 0
flag = False

def retreivePacketAssociation(id):
    p = Packet()
    truckid = Packet.findTruckAssociation(p, id)
    return truckid

def retrievePosition(truckid):
    channel = Truck.channelIDretrieve(Truck(),truckid)
    url = 'https://api.thingspeak.com/channels/'+str(channel)+'/feeds/last'
    pos = json.loads(requests.get(url).content)
    stringa = '{"lat" :' + str(pos['field3']) + ',"long": ' + str(pos['field4']) +'}'
    return stringa

def on_message(msg,chat_id,offset):

    try:
        any(msg['entities'])

    except:
        return

    if msg['entities'][0]['type'] == 'bot_command':

        bot.sendMessage(chat_id,"Enter yuor pack code:")
        time.sleep(10)
        updates = bot.getUpdates(offset)
        if len(updates)!=0:
            trovato = False
            for message in updates:
                if message['message']['chat']['id'] == chat_id:
                    trovato = True
                    packet = (message['message']['text'])

                    if msg['text'] == '/getposition' or msg['text'] == '/getposition@packet_bot':

            # bot.sendMessage(chat_id,"Enter yuor pack code:")
            # time.sleep(10)
            # updates = bot.getUpdates(offset)
            # if len(updates)!=0:
            #     trovato = False
            #     for message in updates:
            #         if message['message']['chat']['id'] == chat_id:
            #             trovato = True
            #             packet = (message['message']['text'])
                        try:
                            truckid = retreivePacketAssociation(str(packet))
                            if truckid != 0:
                                po = retrievePosition(str(truckid))
                                pos = json.loads(po)
                                bot.sendLocation(chat_id, pos['lat'], pos['long'])
                                return

                            else:
                                bot.sendMessage(chat_id, 'Your packet is not in the system')
                                return

                        except Exception as detail:
                            bot.sendMessage(chat_id,"Error in accessing the database")
                            return


                    elif msg['text'] == "/gettemperature" or msg['text'] == "/gettemperature@packet_bot":
                        try:
                            p = Packet()
                            truckid = p.findTruckAssociation(packet)

                            if truckid != 0:
                                t = Truck()
                                s = t.retrieveData(truckid)
                                bot.sendMessage(chat_id,"Temperature = " + s['temperature'] + " C")
                                print (s)
                            else:
                                bot.sendMessage(chat_id, 'Your packet is not in the system')



                        except Exception as detail:
                            bot.sendMessage(chat_id, "Error in accessing the database")
                            return

                    elif msg['text'] == "/gethumidity" or msg['text'] == "/gethumidity@packet_bot":
                        try:
                            p = Packet()
                            truckid = p.findTruckAssociation(packet)

                            if truckid != 0:
                                t = Truck()
                                s = t.retrieveData(truckid)
                                bot.sendMessage(chat_id,"Humidity = " + s['humidity'] + " %")
                                print (s)
                            else:
                                bot.sendMessage(chat_id, 'Your packet is not in the system')



                        except Exception as detail:
                            bot.sendMessage(chat_id, "Error in accessing the database")
                            return

                    elif msg['text'] == "/getall":
                        return

                if trovato == False:
                    bot.sendMessage(chat_id,'Timeout expired! Please try again')



        else:
            bot.sendMessage(chat_id, 'Timeout expired. Please try again')
        #
        # elif msg['text'] == "/gettemperature" or msg['text'] == "/gettemperature@packet_bot":
        #     bot.sendMessage(chat_id, "Enter yuor pack code:")
        #     time.sleep(10)
        #     updates = bot.getUpdates()
        #
        #     if len(updates) != 0:
        #         packet = (updates[len(updates) - 1]['message']['text'])
        #         try:
        #             p = Packet()
        #             truckid = p.findTruckAssociation(packet)
        #
        #             if truckid != 0:
        #                 t = Truck()
        #                 s = t.retrieveData(truckid)
        #                 print (s)
        #             else:
        #                 bot.sendMessage(chat_id, 'Your packet is not in the system')
        #
        #
        #
        #         except Exception as detail:
        #             bot.sendMessage(chat_id, "Error in accessing the database")
        #             return
        #
        #     else:
        #         bot.sendMessage(chat_id, 'Timeout expired. Please try again')
        #         return
        #
        # elif msg['text'] == "/gethumidity":
        #     return
        #
        # elif msg['text'] == "/getall":
        #     return



    else:
        return


if __name__ == '__main__':
    bot = telepot.Bot('378511160:AAF8PCogZt5ZtPUp_gaJU2BPMoWnF6-8zuQ')
    offset = -1
    while True:
        msg = bot.getUpdates(offset)
        if len(msg) != 0:
            offset = msg[0]['update_id']+1
            chat_id,msg_id = telepot.message_identifier(msg[0]['message'])
            on_message(msg[0]['message'],chat_id,offset)
            print (offset)


    #bot.message_loop({'chat':on_message},relax=30,run_forever=True)


