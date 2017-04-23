import telepot
import thread
import time
import datetime

def print_name(chat_id):

    bot.sendMessage(chat_id,'PDB')
    return



if __name__ == '__main__':

    bot = telepot.Bot('378511160:AAF8PCogZt5ZtPUp_gaJU2BPMoWnF6-8zuQ')
    offset = -1
    while True:
        msg = bot.getUpdates(offset)
        if len(msg) != 0:
            offset = msg[0]['update_id']+1
            chat_id,msg_id = telepot.message_identifier(msg[0]['message'])
            print_name(chat_id)
            print (offset)

        else:
            print ('No new')





    #
    # try:
    #     thread.start_new_thread(print_name,('T1',))
    #     thread.start_new_thread(print_name,('T2',))
    # except:
    #     print ('Nada')
    #
    # while 1:
    #     pass