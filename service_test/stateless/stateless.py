from twisted.internet import reactor, defer
from twisted.web.server import Site
from twisted.web.resource import Resource
from txpostgres.txpostgres import ConnectionPool
from twisted.web.server import NOT_DONE_YET
import json

db_config = {
    'host': 'localhost',
    'user': 'wgm',
    'password': 'wgm',
    'port': 5433,
    'database': 'test',
    'min': 10,
    'max': 10,
}
db_pool = None


class GetPlayerByEmail(Resource):
    isLeaf = True

    @defer.inlineCallbacks
    def get_player(self, request):
        sql_args = {
            "email": "vasya@tut.by"
        }
        res = yield db_pool.runQuery("""SELECT * FROM player WHERE email=%(email)s""", sql_args)
        raw_player_info = res[0]
        player_info = {
            "id": raw_player_info[0],
            "name": raw_player_info[1],
            "email": raw_player_info[2],
        }
        player_info_as_json = json.dumps(player_info)
        request.write(player_info_as_json)
        if not request._disconnected:
            request.finish()


    def render_GET(self, request):
        self.get_player(request)
        return NOT_DONE_YET



@defer.inlineCallbacks
def main():
    global db_pool
    db_pool = ConnectionPool('psycopg2', **db_config)
    yield db_pool.start()


if __name__ == "__main__":
    reactor.callWhenRunning(main)
    resource = GetPlayerByEmail()
    factory = Site(resource)
    reactor.listenTCP(8888, factory)
    reactor.run()

