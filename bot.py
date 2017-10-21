from __future__ import print_function
import requests
import json
import time
import telepot
from thingspeak import Truck

# 171602042017

host = 'http://192.168.1.104:8089'
database = 'http://' + requests.get(host + '/database').content + ':8092'
last_processed = 0
flag = False

def retrievePosition(truckid):
    try:
        trucks = json.loads(requests.get(host + '/trucks').content)
    except:
        print ('Error in accessing the catalog. Check your url')
    channel = ''
    for t in trucks:
        if t['channelName'] == str(truckid):
            channel = t['channelID']
            break

    url = 'https://api.thingspeak.com/channels/'+str(channel)+'/feeds/last'
    try:
        pos = json.loads(requests.get(url).content)
        stringa = '{"lat" :' + str(pos['field3']) + ',"long": ' + str(pos['field4']) + '}'
        return stringa
    except:
        print('TS URL not valid. Impossible to connect')


def on_message(msg,chat_id,offset,available_services):

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

                        if 'getposition' in available_services:
                            try:
                                truckid = int(requests.get(database + '/findAssociation?packet='+str(packet)).content)
                                if truckid != 0:
                                    po = retrievePosition(str(truckid)) #todo modify function
                                    pos = json.loads(po)
                                    bot.sendLocation(chat_id, pos['lat'], pos['long'])
                                    return

                                else:
                                    bot.sendMessage(chat_id, 'Your packet is not in the system')
                                    return

                            except Exception as detail:
                                bot.sendMessage(chat_id,"Error in accessing the database")
                                return
                        else:
                            string = 'Operation not available for this service. You can perform:\n'
                            for x in available_services:
                                string += x
                                string += '\n'
                            bot.sendMessage(chat_id,string)



                    elif msg['text'] == "/gettemperature" or msg['text'] == "/gettemperature@packet_bot":
                        if 'gettemperature' in available_services:
                            try:
                                truckid = int(requests.get(database + '/findAssociation?packet='+str(packet)).content)
                                if truckid != 0:
                                    t = Truck()
                                    s = t.retrieveData(truckid)
                                    bot.sendMessage(chat_id,"Temperature = " + s['temperature'] + " C")
                                    print (s)
                                else:
                                    bot.sendMessage(chat_id, 'Your packet is not in the system')

                            except Exception as e:
                                bot.sendMessage(chat_id, "Error in accessing the database")
                                print ('Not albe to connect to the catalogue. Check your connection',e.message)

                                return
                        else:
                            string = 'Operation not available for this service. You can perform:\n'
                            for x in available_services:
                                string += x
                                string += '\n'
                            bot.sendMessage(chat_id,string)

                    elif msg['text'] == "/gethumidity" or msg['text'] == "/gethumidity@packet_bot":
                        if 'gethumidity' in available_services:

                            try:
                                truckid = int(requests.get(database + '/findAssociation?packet='+str(packet)).content)
                                if truckid != 0:
                                    t = Truck()
                                    s = t.retrieveData(truckid)
                                    bot.sendMessage(chat_id,"Humidity = " + s['humidity'] + " %")
                                    print (s)
                                else:
                                    bot.sendMessage(chat_id, 'Your packet is not in the system')

                            except Exception as detail:
                                bot.sendMessage(chat_id, "Error in accessing the database")
                                print ('Not able to connect to the catalog. Check the URL', detail.message)
                                return
                        else:
                            string = 'Operation not available for this service. You can perform:\n'
                            for x in available_services:
                                string += x
                                string += '\n'
                            bot.sendMessage(chat_id,string)


                    elif msg['text'] == '/getall' or msg['text'] == '/getall@packet_bot':
                        if 'getall' in available_services:

                            try:
                                truckid = int(requests.get(database + '/findAssociation?packet='+str(packet)).content)
                                if truckid!=0:
                                    t = Truck()
                                    po = retrievePosition(str(truckid))
                                    pos = json.loads(po)
                                    bot.sendLocation(chat_id, pos['lat'], pos['long'])
                                    s = t.retrieveData(truckid)
                                    bot.sendMessage(chat_id, "Temperature =" + s['temperature'] +  " C\n Humidity = " + s['humidity'] + " %")



                            except Exception as detail:
                                bot.sendMessage(chat_id, "Error in accessing the database")
                                print ('Not able to connect to the catalog. Check the URL', detail.message)
                                return
                        else:
                            string = 'Operation not available for this service. You can perform:\n'
                            for x in available_services:
                                string += x
                                string += '\n'
                            bot.sendMessage(chat_id,string)

                    else:
                        bot.sendMessage(chat_id,'Command not found!')
                        return

                if trovato == False:
                    bot.sendMessage(chat_id,'Timeout expired! Please try again')



        else:
            bot.sendMessage(chat_id, 'Timeout expired. Please try again')

    else:
        return


if __name__ == '__main__':
    bot = telepot.Bot('378511160:AAF8PCogZt5ZtPUp_gaJU2BPMoWnF6-8zuQ')
    offset = -1
    try:
        services = json.loads(requests.get(host +'/telegram').content)
        available_services = []
        for x in services:
            if services[x] == True:
                available_services.append(str(x))
        while True:
            msg = bot.getUpdates(offset)
            if len(msg) != 0:
                offset = msg[0]['update_id']+1
                chat_id,msg_id = telepot.message_identifier(msg[0]['message'])
                on_message(msg[0]['message'],chat_id,offset,available_services)
                print (offset)
    except:
        print('Not able to connect to the catalog. Check your URL')


