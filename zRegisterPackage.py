from __future__ import print_function
from zdatabase import Packet
import requests
import json
import datetime


class RegisterPackage(object):
    """Class used to collect the information about the source and destination,
    generate a unique tracking number for the package and send it to Thingspeak"""

    def __init__(self):

        self.API_KEY = 'FB1E9D1G9CQ658U8'
        self.time = datetime.datetime.today()

    def read(self):

        """Ask for the user to input name, self.mobile and address (street, number and ring).
        Check if the mobile is composed of numbers only (remove " ", "-" and "+").
        If it's not, ask for a new input.
        Return name, mobile and address."""

        # Ask for inputs
        name = raw_input("Name: ").upper()
        mobile = raw_input("Telephone number: ").upper()
        addressStreet = raw_input("Street: ").upper()
        addressNumber = raw_input("Street number: ").upper()
        zip = raw_input("Zip Code:")
        city = raw_input('City:')
        addressRing = raw_input("Ring (leave it empty if there is none): ").upper()

        # Remove some chars of mobile string and check if remain only numbers
        while True:
            try:
                mobile = mobile.replace(" ", "")
                mobile = mobile.replace("+", "")
                mobile = mobile.replace("-", "")
                mobile = int(mobile)
                break

            except:
                print("Invalid telephone number. Type again.")
                mobile = raw_input("Telephone number: ")

        complete_address = addressStreet + " " + addressNumber + " " + zip + " " + city
        geometry = json.loads(
            requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + complete_address).content)

        lat = geometry['results'][0]['geometry']['location']['lat']
        long = geometry['results'][0]['geometry']['location']['lng']

        data = {'name': name,
                'mobile': mobile,
                'street': addressStreet,
                'n_address': addressNumber,
                'zip': zip,
                'city': city,
                'lat': lat,
                'lon': long}
        return data

    def idNumber(self):

        """Generate a number based on timestamp that will be used as the channel
        name of that package"""

        return "%02d%02d%02d%02d%04d" % (
        self.time.minute, self.time.hour, self.time.day, self.time.month, self.time.year)

    def checkData(self):

        """Ask the user to check if the data is correct."""

        print("Name: ", self.name)
        print("Telephone number: ", self.mobile)
        print("Address: %s, %s  %s" % (self.addressStreet, self.addressNumber, self.addressRing))
        print("Check the information. If it is correct type '1' to continue or '0' to cancel")
        correct = raw_input("> ")

        while True:
            if correct == "1":
                return True
            elif correct == "0":
                return False
            else:
                print("Invalid input.")

    def channelIDretrieve(self, truckID):
        channels = requests.get("https://api.thingspeak.com/users/s201586/channels.json").content
        channels_json = json.loads(channels)

        for ch in channels_json["channels"]:
            if ch.get("name") == str(truckID):
                return str(ch.get("id"))


if __name__ == '__main__':
    p = Packet()
    rp = RegisterPackage()
    data = rp.read()
    p.insertPacket(rp.idNumber(), data.get('name'), data.get('street'), data.get('n_address'), data.get('zip'),
                   data.get('city'), data.get('mobile'), data.get('lat'), data.get('lon'))
    p.insertPacketInTruck(rp.idNumber(), '1')

