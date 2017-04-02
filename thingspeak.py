import requests
import json
from database import Packet


class Truck():

    def channelIDretrieve(self,truckID):
        channels = requests.get("https://api.thingspeak.com/users/s201586/channels.json").content
        channels_json = json.loads(channels)

        for ch in channels_json["channels"]:
            if ch.get("name") == str(truckID):
                return str(ch.get("id"))


    def retrieveData(self,truckID):
        channelID = self.channelIDretrieve(truckID)
        url = "https://api.thingspeak.com/channels/" + channelID +"/feeds.json?results=1"
        x = json.loads(requests.get(url).content)
        results = {'temperature' : x["feeds"][0]["field1"],
                   'humidity' : x["feeds"][0]["field2"]}

        return results
