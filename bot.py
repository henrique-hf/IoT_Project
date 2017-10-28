from __future__ import print_function
import requests
import json
import time
import telepot
import cherrypy


host = 'http://192.168.1.109:8089'
try:
    database = 'http://' + requests.get(host + '/database').content + ':8092'
except:
    print ('Connection Error. Not able to reach the catalog for the acquistion of the DB address. Check your URL.')
last_processed = 0
flag = False


def retrieveData(truckID):
    try:
        trucks = json.loads(requests.get(host + '/trucks').content)
    except:
        print ('Error in accessing the catalog. Check your url')
    channel = ''
    for t in trucks:
        if t['channelName'] == str(truckID):
            channel = t['channelID']
            break

    topics = json.loads(requests.get(host + '/topics').content)
    print (topics)
    url = "https://api.thingspeak.com/channels/" + channel + "/feeds/last"
    try:
        x = json.loads(requests.get(url).content)
        print (x)
        results = {'temperature': x[topics['temperature']],
                   'humidity': x[topics['humidity']],
                   'hasovercome_t': x[topics['warning_temp']],
                   'hasovercome_h': x[topics['warning_hum']]}
        return results
    except Exception as e:
        print ('Problem in ThingSpeak Connection! Verify the channelID ',channel,e.message)
        return ('Problem in ThingSpeak Connection! Verify the channelID ',channel,e.message)


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
    print (url)
    try:
        pos = json.loads(requests.get(url).content)
        stringa = '{"lat" :' + str(pos['field3']) + ',"long": ' + str(pos['field4']) + '}'
        return stringa
    except Exception as e:
        print('Problem in ThingSpeak Connection! Verify the channelID ', channel, e.message)
        return ('Problem in ThingSpeak Connection! Verify the channelID ', channel, e.message)


def on_message(msg,chat_id,offset,available_services):

    try:
        any(msg['entities'])

    except:
        return

    if msg['entities'][0]['type'] == 'bot_command':

        bot.sendMessage(chat_id,"Enter your pack code:")

        time.sleep(10)
        updates = bot.getUpdates(offset)
        if len(updates)!=0:
            trovato = False
            for message in updates:
                if message['message']['chat']['id'] == chat_id:
                    trovato = True
                    packet = (message['message']['text'])

                    try:
                        truckid = int(requests.get(database + '/findAssociation?packetid=' + str(packet)).content)
                        print (truckid)
                    except Exception as e:
                        bot.sendMessage(chat_id, 'Connection Error')
                        print('Connection Error. Check the database URL')
                        return

                    if msg['text'] == '/getposition' or msg['text'] == '/getposition@packet_bot':

                        if 'getposition' in available_services:
                            try:
                                print (truckid)
                                if truckid != 0:
                                    po = retrievePosition(str(truckid))
                                    pos = json.loads(po)
                                    bot.sendLocation(chat_id, pos['lat'], pos['long'])
                                    return

                                else:
                                    bot.sendMessage(chat_id, 'Your packet is not in the system')
                                    return

                            except Exception as detail:
                                bot.sendMessage(chat_id,"Error in retrieving position")
                                print ('Error in retrieving position',detail.message)
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
                                if truckid != 0:
                                    s = retrieveData(str(truckid))
                                    bot.sendMessage(chat_id,"Temperature = " + s['temperature'] + " C")

                                    if int(s['hasovercome_t']) == 1:
                                        threshold = json.loads(requests.get(host + '/threshold/'+str(truckid)).content)
                                        print (threshold)
                                        bot.sendMessage(chat_id,'The temperature has overcome the set threshold set at ' + str(threshold['temperature']['threshold_max']))
                                    if int(s['hasovercome_t']) == -1:
                                        threshold = json.loads(requests.get(host + '/threshold/'+str(truckid)).content)
                                        print (threshold)
                                        bot.sendMessage(chat_id,'The temperature has been below the set threshold set at ' + str(threshold['temperature']['threshold_min']))
                                else:
                                    bot.sendMessage(chat_id, 'Your packet is not in the system')

                            except Exception as e:
                                bot.sendMessage(chat_id, e.message)
                                print ('Error',e.message)

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
                                if truckid != 0:
                                    s = retrieveData(truckid)
                                    bot.sendMessage(chat_id,"Humidity = " + s['humidity'] + " %")

                                    if int(s['hasovercome_h']) == 1:
                                        threshold = json.loads(requests.get(host + '/threshold/' + str(truckid)).content)
                                        bot.sendMessage(chat_id,
                                                        'The humidity has overcome the set threshold set at ' + str(threshold['humidity']['threshold_max'])+'%')
                                    if int(s['hasovercome_h']) == -1:
                                        threshold = json.loads(requests.get(host + '/threshold/' + str(truckid)).content)
                                        bot.sendMessage(chat_id,'The temperature has been below the set threshold set at ' + str(threshold['humidity']['threshold_min'])+'%')
                                else:
                                    bot.sendMessage(chat_id, 'Your packet is not in the system')

                            except Exception as detail:
                                bot.sendMessage(chat_id, "Error in accessing the database")
                                print ('Error in accessing the database:', detail.message)
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
                                if truckid!=0:
                                    po = retrievePosition(str(truckid))
                                    pos = json.loads(po)
                                    bot.sendLocation(chat_id, pos['lat'], pos['long'])
                                    s = retrieveData(truckid)
                                    bot.sendMessage(chat_id, "Temperature =" + s['temperature'] +  " C\n Humidity = " + s['humidity'] + " %")

                                    if s['hasovercome_t'] == 1:
                                        threshold = json.loads(requests.get(host + '/threshold').content)
                                        bot.sendMessage(chat_id,'The temperature has overcome the set threshold set at' + str(threshold['temperature']))

                                    if s['hasovercome_h'] == 1:
                                        threshold = json.loads(requests.get(host + '/threshold').content)
                                        bot.sendMessage(chat_id,'The humidity has overcome the set threshold set at' + str(threshold['humidity']))


                            except Exception as detail:
                                bot.sendMessage(chat_id, "Error in accessing the database")
                                print ('Error in accessing the database', detail.message)
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
    #time.sleep(10)
    bot = telepot.Bot('378511160:AAF8PCogZt5ZtPUp_gaJU2BPMoWnF6-8zuQ')
    offset = -1
    try:
        services = json.loads(requests.get(host +'/telegram').content)
    except:
        print('Not able to connect to the catalog. Check your URL')
        exit()
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
