import requests
import json
import cherrypy

host = '192.168.1.112'
homeCatalog = 'http://192.168.1.112:8088'
url = 'https://api.thingspeak.com/channels/'


class Statistics(object):
    exposed = True

    def __init__(self):
        self.topics = json.loads(requests.get(homeCatalog + '/topics').content)
        self.trucks = json.loads(requests.get(homeCatalog + '/trucks').content)

    def statistics(self, truck):
        for channel in self.trucks:
            if str(truck) == channel['channelName']:
                channelID = channel['channelID']
                break

        data = json.loads(requests.get(url + channelID + '/feeds.json').content)

        # TEMPERATURE
        fieldTemp = self.topics['temperature']

        listTemp = []

        for i in data['feeds']:
            try:
                listTemp.append(float(i[fieldTemp]))
            except:
                print 'Problem with temperature value: ' + i[fieldTemp]

        sum = 0
        for element in listTemp:
            sum = sum + element

        averageTemp = sum / len(listTemp)

        # HUMIDITY
        fieldHum = self.topics['humidity']

        listHum = []

        for i in data['feeds']:
            try:
                listHum.append(float(i[fieldHum]))
            except:
                print 'Problem with humidity value: ' + i[fieldHum]

        sum = 0
        for element in listHum:
            sum = sum + element

        averageHum = sum / len(listHum)

        # WARNINGS TEMPERATURES
        fieldWarningTemp = self.topics['warning_temp']

        listWarningsTemp = []

        for i in data['feeds']:
            try:
                listWarningsTemp.append(float(i[fieldWarningTemp]))
            except:
                print 'Problem with warning temperature value: ' + i[fieldWarningTemp]

        belowTemp = 0
        aboveTemp = 0
        for element in listWarningsTemp:
            if element == 1:
                aboveTemp = aboveTemp + 1
            elif element == -1:
                belowTemp = belowTemp + 1

        totalTemp = aboveTemp + belowTemp

        percentageTemp = 1 - (float(totalTemp) / len(listWarningsTemp))

        # WARNING HUMIDITY
        fieldWarningHum = self.topics['warning_hum']

        listWarningsHum = []

        for i in data['feeds']:
            try:
                listWarningsHum.append(float(i[fieldWarningHum]))
            except:
                print 'Problem with warning humidity value: ' + i[fieldWarningHum]

        belowHum = 0
        aboveHum = 0
        for element in listWarningsHum:
            if element == 1:
                aboveHum = aboveHum + 1
            elif element == -1:
                belowHum = belowHum + 1

        totalHum = aboveHum + belowHum

        percentageHum = 1 - (float(totalHum) / len(listWarningsHum))

        return json.dumps({'averageTemp': averageTemp, 'averageHum': averageHum, 'warningTemp': {'below': belowTemp, \
                    'above': aboveTemp, 'total': totalTemp, 'percentage': round(percentageTemp,2)}, 'warningHum': \
                    {'below': belowHum, 'above': aboveHum, 'total': totalHum, 'percentage': round(percentageHum, 2)}})

    def GET(self,*uri, **param):
        if uri[0] == 'statistics':
            return self.statistics(param['truck'])


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