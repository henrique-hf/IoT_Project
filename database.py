import requests
import json
import datetime
import pymysql
import cherrypy

class Packet(object):
    exposed = True
    # try:
    #     db = pymysql.connect(host="127.0.0.1",user="root", passwd="",db="tracking")
    #     cursor = db.cursor()
    #     cursor.execute("SHOW DATABASES")
    #     a = cursor.execute("SELECT * FROM tracking.truck")
    #
    #     print (cursor.fetchone())
    # except:
    #     print ('Error in reading database')

    def GET(self, *uri,**params):

        complete_address = params['address'] + " " + params['nr'] + " " + params['zip'] + " " + params['city']
        geometry = json.loads(
            requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + complete_address).content)

        lat = geometry['results'][0]['geometry']['location']['lat']
        long = geometry['results'][0]['geometry']['location']['lng']


        self.insertPacket(self.idNumber(),params['name'],params['address'],params['nr'],params['zip'],params['city'],params['telephone'])#,lat,long)

    def idNumber(self):
        time = datetime.datetime.today()
        """Generate a number based on timestamp that will be used as the channel
        name of that package"""

        return "%02d%02d%02d%02d%04d" % (
        time.minute, time.hour, time.day, time.month, time.year)

    def insertPacket(self,packet,name,address,n_address,zip,city,telephone):#,lat,lon):
        script = "INSERT INTO `tracking`.`packet` (`packetid`, `name`, `address`,`n_address`, `zip`, `city`, `telephone`) VALUES ("
        # script = "INSERT INTO `tracking`.`packet` (`packetid`, `name`, `address`,`n_address`, `zip`, `city`, `telephone`,`lat`,`long`) VALUES ("
        script += "\'" + str(packet) + "\',"
        script += "'" + name + "',"
        script += "'" + address + "',"
        script += "'" + str(n_address) + "',"
        script += "'" + str(zip) + "',"
        script += "'" + city + "',"
        script += "'" + str(telephone) + "')"
        print (script)
       # script += "'" + str(lat) + "',"
       # script += "'" + str(lon) + "')"


        try:
            db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="tracking")
            cursor = db.cursor()
            #cursor.execute("SELECT * FROM `tracking`.`packet`")
            #print (cursor.fetchall())
            cursor.execute(script)
            db.commit()
            # cursor.execute("SELECT * FROM `tracking`.`packet`")
            # print (cursor.fetchall())
            db.close()

        except Exception as e:
            print ('Error in reading database',e)


    def findPacket(self,packetid):
        script = 'SELECT `packetid` FROM `tracking`.`packet` WHERE `packetid`=\'' + str(packetid) + '\';'
        print (script)
        try:
            db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="tracking")
            cursor = db.cursor()
            cursor.execute(script)
            x = cursor.fetchone()
            db.close()
            if x is None:
                return 0
            else:
                return 1

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




if __name__ == "__main__":



        conf = {
            "/": {
                "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
                "tools.sessions.on": True,
                }
            }
        cherrypy.tree.mount (Packet(), "/", conf)
        cherrypy.config.update({
            "server.socket_host": 'localhost',
            "server.socket_port": 8089})

        cherrypy.engine.start()
        cherrypy.engine.block()
