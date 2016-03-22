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
}
db_pool = None

EMAIL = "vasya@tut.by"
PLAYERS = {}

class GetPlayerByEmail(Resource):
    isLeaf = True

    def get_player(self, email):
        return PLAYERS[email]


    def render_GET(self, request):
        player = self.get_player(EMAIL)
        return json.dumps(player)


@defer.inlineCallbacks
def main():
    global db_pool
    db_pool = ConnectionPool('psycopg2', **db_config)
    yield db_pool.start()
    sql_args = {
        "email": EMAIL
    }
    res = yield db_pool.runQuery("""SELECT * FROM player""")
    for raw_player_info in res:
        email = raw_player_info[2]
        player_info = {
            "id": raw_player_info[0],
            "name": raw_player_info[1],
            "email": email
        }
        PLAYERS[email] = player_info


if __name__ == "__main__":
    reactor.callWhenRunning(main)
    resource = GetPlayerByEmail()
    factory = Site(resource)
    reactor.listenTCP(8888, factory)
    reactor.run()

