import random
import cherrypy
import requests
import urllib2
import json
import datetime

class RegisterPackage(object):
    exposed = True;

    """Class used to collect the information about the source and destination,
    generate a unique tracking number for the package and send it to Thingspeak"""

    def __init__(self):

        self.API_KEY = '7C2YGM6HF9E63AG2'


    def read(self):

        """Ask for the user to input name, self.mobile and address (street, number and ring).
        Check if the mobile is composed of numbers only (remove " ", "-" and "+").
        If it's not, ask for a new input.
        Return name, mobile and address."""

        #Ask for inputs
        self.name = raw_input("Name: ").upper()
        self.mobile = raw_input("Telephone number: ").upper()
        self.addressStreet = raw_input("Street: ").upper()
        self.addressNumber = raw_input("Street number: ").upper()
        self.addressRing = raw_input("Ring (leave it empty if there is none): ").upper()

        #Remove some chars of mobile string and check if remain only numbers
        while True:
            try:
                self.mobile = self.mobile.replace(" ", "")
                self.mobile = self.mobile.replace("+", "")
                self.mobile = self.mobile.replace("-", "")
                self.mobile = int(self.mobile)
                break

            except:
                print ("Invalid telephone number. Type again.")
                self.mobile = raw_input("Telephone number: ")

        return self.name, self.mobile, self.addressStreet, self.addressNumber, self.addressRing


    def idNumber(self):

        """Generate a random number that will be used as an ID for the package and check if that
        number hasn't been used before for other package."""

        time = datetime.datetime.today()

        return time.


    def checkData(self):

        """Ask the user to check if the data is correct."""

        print "Name: ", self.name
        print "Telephone number: ", self.mobile
        print "Address: %s, %s  %s" % (self.addressStreet, self.addressNumber, self.addressRing)
        print "Check the information. If it is correct type '1' to continue or '0' to cancel"
        correct = raw_input("> ")

        while True:
            if correct == "1":
                return True
            elif correct == "0":
                return False
            else:
                print ("Invalid input.")


    def POST(self):
        url = "https://api.thingspeak.com/channels?api_key="
        requests.post(url)
        # api_key = XXXXXXXXXXXXXXXX
        # name = My
        # New
        # Channel

    #def PUT(self):


    def GET(self,*uri,*params):

        """Get the list of channels created before"""

        url = "https://thingspeak.com/channels.json?api_key=7C2YGM6HF9E63AG2"

        a = requests.get(url).content

        return a


if __name__ == '__main__':



