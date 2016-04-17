from aiohttp import web

async def handle(request):
    text = "pong"
    return web.Response(body=text.encode('utf-8'))



app = web.Application()
app.router.add_route('GET', '/', handle)

web.run_app(app, port=8888)
