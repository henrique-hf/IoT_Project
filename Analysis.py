import requests
import json
import cherrypy

host = '192.168.1.109'
homeCatalog = 'http://192.168.1.109:8089'
url = 'https://api.thingspeak.com/channels/'


class Statistics(object):

    def __init__(self):
        self.topics = json.loads(requests.get(homeCatalog + '/topics').content)
        self.trucks = json.loads(requests.get(homeCatalog + '/trucks').content)

    def averageTemp(self, truck):
        field = self.topics['temperature']
        fieldOnlyNum = field.replace('field', '')

        for channel in self.trucks:
            if str(truck) == channel['channelName']:
                channelID = channel['channelID']
                break

        data = json.loads(requests.get(url + channelID + '/fields/' + fieldOnlyNum + '.json').content)

        listTemp = []

        for i in data['feeds']:
            listTemp.append(float(i[field]))

        sum = 0
        for element in listTemp:
            sum = sum + element

        averageTemp = sum / len(listTemp)

        return averageTemp

    def averageHum(self, truck):
        field = self.topics['humidity']
        fieldOnlyNum = field.replace('field', '')

        for channel in self.trucks:
            if str(truck) == channel['channelName']:
                channelID = channel['channelID']
                break

        data = json.loads(requests.get(url + channelID + '/fields/' + fieldOnlyNum + '.json').content)

        listHum = []

        for i in data['feeds']:
            listHum.append(float(i[field]))

        sum = 0
        for element in listHum:
            sum = sum + element

        averageHum = sum / len(listHum)

        return averageHum

    def warningsTemp(self, truck):
        field = self.topics['warning_temp']
        fieldOnlyNum = field.replace('field', '')

        for channel in self.trucks:
            if str(truck) == channel['channelName']:
                channelID = channel['channelID']
                break

        data = json.loads(requests.get(url + channelID + '/fields/' + fieldOnlyNum + '.json').content)

        listWarningsTemp = []

        for i in data['feeds']:
            listWarningsTemp.append(float(i[field]))

        below = 0
        above = 0
        for element in listWarningsTemp:
            if element == 1:
                above = above + 1
            elif element == -1:
                below = below + 1

        total = above + below

        percentage = 1 - (float(total) / len(listWarningsTemp))

        return json.dumps({'below': below, 'above': above, 'total': total, 'percentage': round(percentage,2)})

    def warningsHum(self, truck):
        field = self.topics['warning_hum']
        fieldOnlyNum = field.replace('field', '')

        for channel in self.trucks:
            if str(truck) == channel['channelName']:
                channelID = channel['channelID']
                break

        data = json.loads(requests.get(url + channelID + '/fields/' + fieldOnlyNum + '.json').content)

        listWarningsHum = []

        for i in data['feeds']:
            listWarningsHum.append(float(i[field]))

        below = 0
        above = 0
        for element in listWarningsHum:
            if element == 1:
                above = above + 1
            elif element == -1:
                below = below + 1

        total = above + below

        percentage = 1 - (float(total) / len(listWarningsHum))

        return json.dumps({'below': below, 'above': above, 'total': total, 'percentage': round(percentage,2)})


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True,
        }
    }
    cherrypy.tree.mount(Statistics(), "/", conf)
    cherrypy.config.update({
        "server.socket_host": host,
        "server.socket_port": 8089})
    cherrypy.engine.start()
    cherrypy.engine.block()


# x = Statistics()
#
# averageTem = x.averageTemp(1)
# averageHum = x.averageHum(1)
# warningTemp = x.warningsTemp(1)
# warningHum = x.warningsHum(1)
#
# print averageTem
# print averageHum
# print warningTemp
# print warningHum