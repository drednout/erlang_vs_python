from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource


class PingPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        return "PONG"

resource = PingPage()
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run()
