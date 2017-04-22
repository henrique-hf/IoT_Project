import pymysql
import requests
import json

class Packet():
    # try:
    #     db = pymysql.connect(host="127.0.0.1",user="root", passwd="",db="tracking")
    #     cursor = db.cursor()
    #     cursor.execute("SHOW DATABASES")
    #     a = cursor.execute("SELECT * FROM tracking.truck")
    #
    #     print (cursor.fetchone())
    # except:
    #     print ('Error in reading database')

    def insertPacket(self,packet,name,address,zip,city,telephone):

        script = "INSERT INTO `tracking`.`packet` (`packetid`, `name`, `address`, `zip`, `city`, `telephone`) VALUES ("
        script += "'" + str(packet) + "',"
        #script += "'" + str(truck) + "',"
        script += "'" + name + "',"
        script += "'" + address + "',"
        script += "'" + str(zip) + "',"
        script += "'" + city + "',"
        script += "'" + str(telephone) + "')"

        print script

        try:
            db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="tracking")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM `tracking`.`packet`")
            print cursor.fetchall()
            cursor.execute(script)
            db.commit()
            cursor.execute("SELECT * FROM `tracking`.`packet`")
            print cursor.fetchall()
            db.close()

        except:
            print ('Error in reading database')


    def deletePacket(self,packetid):
        script = "DELETE FROM `tracking`.`packet` WHERE `packetid`='" + str(packetid) + "';"
        try:
            db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="tracking")
            cursor = db.cursor()
            cursor.execute(script)
            db.commit()
            cursor.execute("SELECT * FROM `tracking`.`packet`")
            print cursor.fetchall()
            db.close()

        except:
            print ('Error in reading database')


    def insertPacketInTruck(self,packetid,truckid):
        script = "INSERT INTO `tracking`.`p_t` (`packetid`, `truckid`) VALUES ('" + packetid +"', '" + truckid+ "');"

        try:
            db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="tracking")
            cursor = db.cursor()
            cursor.execute(script)
            db.commit()
            cursor.execute("SELECT * FROM `tracking`.`p_t`")
            print cursor.fetchall()
            db.close()

        except:
            print ('Error in reading database')

    def findTruckAssociation(self,packet):

        script = 'SELECT truckid FROM p_t' \
                 ' WHERE packetid = ' + packet

        try:
            db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="tracking")
            cursor = db.cursor()
            cursor.execute(script)
            x = cursor.fetchone()
            db.close()
            if x is None:
                return 0
            else:
                truckid = x[0]
                return truckid

        except:
            print ('Error in reading database')



    def channelIDretrieve(self, truckID):
        channels = requests.get("https://api.thingspeak.com/users/s201586/channels.json").content
        channels_json = json.loads(channels)

        for ch in channels_json["channels"]:
            if ch.get("name") == str(truckID):
                return str(ch.get("id"))


# if __name__ == "__main__":
#     p = Packet()
#     p.findTruckAssociation('25')
#     p.deletePacket(1)
#
