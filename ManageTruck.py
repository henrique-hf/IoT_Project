import requests
import json

class ManageTruck():

    def __init__(self):
        # user's api key needed to create/remove channels
        self.apiKey = '7C2YGM6HF9E63AG2'
        self.names = []
        self.nextName = 0

    def getName(self):
        # get a list of all existing channels
        jsonChannels = requests.get('https://api.thingspeak.com/channels.json?api_key=' + self.apiKey).content
        channels = json.loads(jsonChannels)
        for i in channels:
            self.names.append(i['name'])
        self.nextName = int(self.names[-1]) + 1
        return self.nextName

    def add(self, name):
        # set name and the relevant fields of the new channel - convert to json
        data = {'name': name, 'api_key': self.apiKey, 'public_flag': 'true', 'field1': 'Temperature', 'field2': 'Humidity',
                'field3': 'Latitude', 'field4': 'Longitude'}
        jsonData = json.dumps(data)
        # send the POST request to create the new channel
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        channel = requests.post('https://api.thingspeak.com/channels.json', data=jsonData, headers=headers)
        return channel

    def remove(self, channelID):
        # send a DELETE request to remove one existing channel - pass channel ID as parameter
        data = {'api_key': self.apiKey}
        channel = requests.delete('https://api.thingspeak.com/channels/' + channelID + '.json', params=data)
        return channel

    #def edit(self):

if __name__ == '__main__':
    truck = ManageTruck()

    #channel = truck.add('Truck 6')
    #print channel

    #channel = truck.remove('263661')
    #print channel

    name = truck.getName()
    print name
    # channel = truck.add(name)
    # print channel
