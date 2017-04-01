import pymysql


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


    def insertPacket(self,packet,truck,name,address,zip,city,telephone):
        script = "INSERT INTO `tracking`.`packet` (`packetid`, `truckid`, `name`, `address`, `zip`, `city`, `telephone`) VALUES ("
        script += "'" + str(packet) + "',"
        script += "'" + str(truck) + "',"
        script += "'" + name + "',"
        script += "'" + address + "',"
        script += "'" + str(zip) + "',"
        script += "'" + city + "',"
        script += "'" + str(telephone) + "')"

        try:
            db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="tracking")
            cursor = db.cursor()
            cursor.execute("SHOW DATABASES")
            a = cursor.execute("SELECT * FROM tracking.truck")

            print (cursor.fetchone())
        except:
            print ('Error in reading database')

        try:
            cursor.execute(script)
            a = cursor.execute("SELECT * FROM tracking.packet")
            print cursor.fetchall()
        except:
            print ('Errore nella query')


   # DELETE FROM `tracking`.`packet` WHERE `packetid`='1';

   # INSERT INTO `tracking`.`packet` (`packetid`, `truckid`, `name`, `address`, `zip`, `city`, `telephone`) VALUES ('', '1', 'Mario Rossi', 'Via Matteotti 1', '10125', 'Torino', '123456789');


if __name__ == "__main__":
    p = Packet()
    p.insertPacket(2,1,'a','c',2,'b',3)

