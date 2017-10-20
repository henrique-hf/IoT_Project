from __future__ import print_function
import requests
import json
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from zdatabase import Packet
from thingspeak import Truck

# 171602042017

class Bot():
    def __init__(self,token,offset):
        self.token = token
        self.offset = offset
        self.saved_packet = {}
        self.bot = telepot.Bot(token)
        self.botcommand = ['/getposition', '/getposition@packet_bot',
                           '/gettemperature','/gettemperature@packet_bot',
                           '/gethumidity', '/gethumidity@packet_bot',
                           '/getall', '/getall@packet_bot',
                           '/setpacket', '/setpacket@packet_bot',
                           '/changepacket','/changepacket@packet_bot'
                           ]

    def retreivePacketAssociation(self,id):
        p = Packet()
        truckid = Packet.findTruckAssociation(p, id)
        return truckid

    def retrievePosition(self,truckid):
        channel = Truck.channelIDretrieve(Truck(),truckid)
        url = 'https://api.thingspeak.com/channels/'+str(channel)+'/feeds/last'
        pos = json.loads(requests.get(url).content)
        stringa = '{"lat" :' + str(pos['field3']) + ',"long": ' + str(pos['field4']) +'}'
        return stringa

    def on_message(self,msg,chat_id,offset):

        try:
            any(msg['entities'])

        except:
            return

        if msg['entities'][0]['type'] == 'bot_command':
            if msg['text'] in self.botcommand:
                if self.saved_packet.get(chat_id) == None or msg['text']=='/changepacket' or msg['text']=='/changepacket@packet_bot':
                    self.bot.sendMessage(chat_id,"Enter yuor pack code:")
                    time.sleep(10)
                    updates = self.bot.getUpdates(offset)
                    if len(updates)!=0:
                        trovato = False
                        for message in updates:
                            if message['message']['chat']['id'] == chat_id:
                                packet = (message['message']['text'])
                                trovato = True

                        if trovato == False :
                            self.bot.sendMessage(chat_id, 'Timeout expired! Please try again')
                            return

                else:
                    packet = self.saved_packet.get(chat_id)

                if msg['text'] == '/getposition' or msg['text'] == '/getposition@packet_bot':

                    try:
                        truckid = self.retreivePacketAssociation(str(packet))
                        if truckid != 0:
                            po = self.retrievePosition(str(truckid))
                            pos = json.loads(po)
                            self.bot.sendLocation(chat_id, pos['lat'], pos['long'])
                            return

                        else:
                            self.bot.sendMessage(chat_id, 'Your packet is not in the system')
                            return

                    except Exception as detail:
                        self.bot.sendMessage(chat_id,"Error in accessing the database")
                        return

                elif msg['text'] == "/setpacket" or msg['text'] == "/setpacket@packet_bot":
                    p = Packet()

                    if p.findPacket(packet):
                        self.saved_packet[chat_id] = packet
                        self.bot.sendMessage(chat_id,'Packet: ' + str(packet))
                        return
                    else:
                        #self.saved_packet.__delattr__(chat_id)
                        self.bot.sendMessage(chat_id,'Your packet is not in the system')
                        return

                elif  msg['text'] == '/changepacket' or msg['text'] == '/changepacket@packet_bot':
                    p = Packet()
                    old = self.saved_packet.get(chat_id)
                    if p.findPacket(packet):
                        self.saved_packet[chat_id] = packet
                        self.bot.sendMessage(chat_id,'You were following the #'+str(old)+'\nNow your packet is the #' + str(packet))
                        return
                    else:
                        #self.saved_packet.__delattr__(chat_id)
                        self.bot.sendMessage(chat_id,'Your packet is not in the system')
                        return



                elif msg['text'] == "/gettemperature" or msg['text'] == "/gettemperature@packet_bot":
                    try:
                        p = Packet()
                        truckid = p.findTruckAssociation(packet)

                        if truckid != 0:
                            t = Truck()
                            s = t.retrieveData(truckid)
                            self.bot.sendMessage(chat_id,"Temperature = " + s['temperature'] + " C")
                            print (s)
                            return
                        else:
                            self.bot.sendMessage(chat_id, 'Your packet is not in the system')
                            return



                    except Exception as detail:
                        self.bot.sendMessage(chat_id, "Error in accessing the database")
                        return

                elif msg['text'] == "/gethumidity" or msg['text'] == "/gethumidity@packet_bot":
                    try:
                        p = Packet()
                        truckid = p.findTruckAssociation(packet)

                        if truckid != 0:
                            t = Truck()
                            s = t.retrieveData(truckid)
                            self.bot.sendMessage(chat_id,"Humidity = " + s['humidity'] + " %")
                            print (s)
                            return
                        else:
                            self.bot.sendMessage(chat_id, 'Your packet is not in the system')
                            return

                    except Exception as detail:
                        self.bot.sendMessage(chat_id, "Error in accessing the database")
                        return


                elif msg['text'] == '/getall' or msg['text'] == '/getall@packet_bot':
                    try:
                        p = Packet()
                        truckid = p.findTruckAssociation(packet)

                        if truckid!=0:
                            t = Truck()
                            po = self.retrievePosition(str(truckid))
                            pos = json.loads(po)
                            self.bot.sendLocation(chat_id, pos['lat'], pos['long'])
                            s = t.retrieveData(truckid)
                            self.bot.sendMessage(chat_id, "Temperature =" + s['temperature'] +  " C\n Humidity = " + s['humidity'] + " %")
                            return


                    except Exception as detail:
                        self.bot.sendMessage(chat_id, "Error in accessing the database")
                        return

            elif msg['text'] == '/getpacket' or msg['text'] == '/getpacket@packetbot':
                if self.saved_packet.get(chat_id):
                    self.bot.sendMessage(chat_id,self.saved_packet.get(chat_id))
                    return

                else:
                    self.bot.sendMessage(chat_id,'You did not save any packet. To set a packet use /setpacket')
                    return

            elif msg['text'] == '/deletepacket' or msg['text'] == '/deletepacket@packet_bot':

                if not self.saved_packet.get(chat_id):
                    self.bot.sendMessage(chat_id,'No packet was setted as default')
                    return

                toremove = self.saved_packet.get(chat_id)

                self.saved_packet.pop(chat_id)

                self.bot.sendMessage(chat_id,'Packet ' + str(toremove) + ' is not set as default anymore' )

            else:
                self.bot.sendMessage(chat_id,'Command not found!')
                return

        else:
            self.bot.sendMessage(chat_id, 'Timeout expired. Please try again')
            return

    def getUpdates(self):
        while True:
            msg = self.bot.getUpdates(self.offset)
            if len(msg) != 0:
                self.offset = msg[0]['update_id']+1
                chat_id,msg_id = telepot.message_identifier(msg[0]['message'])
                self.on_message(msg[0]['message'],chat_id,offset)
                print (self.offset)

if __name__ == '__main__':
    token = '378511160:AAF8PCogZt5ZtPUp_gaJU2BPMoWnF6-8zuQ'
    offset = -1
    b = Bot(token,offset)
    b.getUpdates()



    #bot.message_loop({'chat':on_message},relax=30,run_forever=True)


