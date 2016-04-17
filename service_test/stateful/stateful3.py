import json
import asyncio
import aiopg
from aiohttp import web


db_pool = None

EMAIL = "vasya@tut.by"
PLAYERS = {}

async def handle(request):
    player = PLAYERS[EMAIL]
    text = json.dumps(player)
    return web.Response(body=text.encode('utf-8'))


async def init():
    global db_pool
    dsn = 'dbname=test user=wgm password=wgm port=5433 host=127.0.0.1'
    db_pool = await aiopg.create_pool(dsn, minsize=10)
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""SELECT * FROM player""")
            async for raw_player_info in cur:
                email = raw_player_info[2]
                player_info = {
                    "id": raw_player_info[0],
                    "name": raw_player_info[1],
                    "email": raw_player_info[2],
                }
                PLAYERS[email] = player_info

loop = asyncio.get_event_loop()
loop.run_until_complete(init())


app = web.Application()
app.router.add_route('GET', '/', handle)

web.run_app(app, port=8888)
