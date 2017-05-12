import requests
import json
import datetime
import pymysql
import cherrypy
from thingspeak import Truck
import requests
import webbrowser


class Packet(object):
    exposed = True

    def GET(self, *uri,**params):

        if uri[0] == 'findPacket':
            if self.findPacket(params['packetid']):
                print (params['packetid'])
                truckid = self.findTruckAssociation(params['packetid'])
                channel = self.channelIDretrieve(truckid)
                position = self.retrievePosition(truckid)
                webbrowser.open_new_tab('http://localhost/maps.php/?lat='+str(position['lat'])+'&long='+str(position['long'])+'&channel='+channel)
                #print ('http://localhost/maps.php/?lat='+str(position['lat'])+'&long='+str(position['long']))


            else:
                print 'The id inserted is not valid!'

        if uri[0] == 'create':
            complete_address = params['address'] + " " + params['nr'] + " " + params['zip'] + " " + params['city']
            geometry = json.loads(
                requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + complete_address).content)

            lat = geometry['results'][0]['geometry']['location']['lat']
            long = geometry['results'][0]['geometry']['location']['lng']


            self.insertPacket(self.idNumber(),params['name'],params['address'],params['nr'],params['zip'],params['city'],params['telephone'],lat,long)

            return json.dumps(params) + ' INSERTED'

        if uri[0] == 'associate':
            if self.findPacket(params['packetid']):
                try:
                    self.insertPacketInTruck(params['packetid'],params['truckid'])
                    return 'Packet ' + params['packetid'] + ' inserted in truck ' + params['truckid']
                except:
                    return 'Error in inserting the packet'
            else:
                return 'Packet not present in the system'

        if uri[0] == 'delivered':
            if self.findPacket(params['packetid']):
                try:
                    self.packetDelivered(params['packetid'],params['truckid'])
                    return 'Packet ' + params['packetid'] + ' delivered ' + params['truckid']
                except:
                    return 'Error in inserting the packet'
            else:
                return 'Packet not present in the system'

    def idNumber(self):
        time = datetime.datetime.today()
        """Generate a number based on timestamp that will be used as the channel
        name of that package"""

        return "%04d%02d%02d%02d%02d%02d" % (
        time.year,time.month, time.day, time.hour, time.minute, time.second)

    def insertPacket(self,packet,name,address,n_address,zip,city,telephone,lat,lon):
        script = "INSERT INTO `tracking`.`packet` (`packetid`, `name`, `address`,`n_address`, `zip`, `city`, `telephone`,`lat`,`long`) VALUES ("
        script += "\'" + str(packet) + "\',"
        script += "'" + name + "',"
        script += "'" + address + "',"
        script += "'" + str(n_address) + "',"
        script += "'" + str(zip) + "',"
        script += "'" + city + "',"
        script += "'" + str(telephone) + "',"
        script += "'" + str(lat) + "',"
        script += "'" + str(lon) + "')"


        try:
            db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="tracking")
            cursor = db.cursor()
            cursor.execute(script)
            db.commit()
            print_script = 'SELECT * FROM tracking.packet as tp ORDER BY tp.packetid desc'
            cursor.execute(print_script)
            for row in cursor.fetchall():
                print (row)
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


    def packetDelivered(self,packet,truck):
        script = "UPDATE `tracking`.`p_t` SET `delivered`='1' WHERE `packetid`='"+ packet + "' and`truckid`='"+truck+"';"
        try:
            db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="tracking")
            cursor = db.cursor()
            cursor.execute(script)
            db.commit()
            cursor.execute("SELECT * FROM `tracking`.`p_t`")
            db.close()

        except:
            print ('Error in reading database')


    def channelIDretrieve(self, truckID):
        channels = requests.get("https://api.thingspeak.com/users/s201586/channels.json").content
        channels_json = json.loads(channels)

        for ch in channels_json["channels"]:
            if ch.get("name") == str(truckID):
                return str(ch.get("id"))

    def retreivePacketAssociation(self,packetid):
        truckid = self.findTruckAssociation(packetid)
        return truckid

    def retrievePosition(self,truckid):
        channel = Truck.channelIDretrieve(Truck(), truckid)
        url = 'https://api.thingspeak.com/channels/' + str(channel) + '/feeds/last'
        pos = json.loads(requests.get(url).content)
        stringa = '{"lat" :' + str(pos['field3']) + ',"long": ' + str(pos['field4']) + '}'
        d = json.loads(stringa)
        return d




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
            "server.socket_port": 8082})

        cherrypy.engine.start()
        cherrypy.engine.block()
