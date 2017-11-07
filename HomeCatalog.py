import cherrypy
import json

host = '192.168.1.100'

class Catalog(object):
    exposed = True

    def __init__(self):
        self.file = open("catalog.json", "r")
        self.catalog = json.load(self.file)
        self.file.close()

    def GET(self, *uri):
        # OK
        if uri[0] == 'topics':
            print self.catalog['topics']
            print type(self.catalog['topics'])
            return json.dumps(self.catalog['topics'])

        # OK
        elif uri[0] == 'broker':
            print self.catalog['broker']
            print type(self.catalog['broker'])
            return self.catalog['broker']['address']

        # OK
        elif uri[0] == 'telegram':
            print self.catalog['telegram']
            print type(self.catalog['telegram'])
            return json.dumps(self.catalog['telegram'])

        # OK
        elif uri[0] == 'key':
            print self.catalog['key']
            print type(self.catalog['key'])
            return self.catalog['key']

        # OK
        elif uri[0] == 'user':
            print self.catalog['user']
            print type(self.catalog['user'])
            return self.catalog['user']

        # OK
        elif uri[0] == 'sensor':
            for truck in self.catalog['trucks']:
                if uri[1] == truck['raspberry']:
                    return json.dumps(truck)

        elif uri[0] == 'database':
            print self.catalog['database']
            print type(self.catalog['database'])
            return self.catalog['database']

        elif uri[0] == 'analysis':
            print self.catalog['analysis']
            return self.catalog['analysis']

        elif uri[0] == 'trucks':
            print self.catalog['trucks']
            print type(self.catalog['trucks'])
            return json.dumps(self.catalog['trucks'])
        
        elif uri[0] == 'stringTrucks':
            string = ""
            for truck in self.catalog['trucks']:
                string = string + "," + truck['channelName']
            return string

        elif uri[0] == 'threshold':
            threshold = {'humidity': {'threshold_max': 100, 'threshold_min': 0}, 'temperature': {'threshold_max': 100, 'threshold_min': 0}}
            for truck in self.catalog['trucks']:
                if truck['channelName'] == uri[1]:
                    threshold['humidity']["threshold_max"] = truck['humidity']['threshold_max']
                    threshold['humidity']["threshold_min"] = truck['humidity']['threshold_min']
                    threshold['temperature']["threshold_max"] = truck['temperature']['threshold_max']
                    threshold['temperature']["threshold_min"] = truck['temperature']['threshold_min']
            return json.dumps(threshold)


if __name__ == "__main__":
        conf = {
            "/": {
                "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
                "tools.sessions.on": True,
                }
            }
        cherrypy.tree.mount(Catalog(), "/", conf)
        cherrypy.config.update({
            "server.socket_host": host,
            "server.socket_port": 8089})
        cherrypy.engine.start()
        cherrypy.engine.block()
