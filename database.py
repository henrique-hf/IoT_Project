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


    def packetInTruck(self,packetid,truckid):
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


   # INSERT INTO `tracking`.`packet` (`packetid`, `truckid`, `name`, `address`, `zip`, `city`, `telephone`) VALUES ('', '1', 'Mario Rossi', 'Via Matteotti 1', '10125', 'Torino', '123456789');


# if __name__ == "__main__":
#     p = Packet()
#     p.insertPacket(2,1,'a','c',2,'b',3)
#     p.deletePacket(1)

