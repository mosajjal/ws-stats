import asyncio
import json
from pathlib import Path

import websockets
from aiohttp import web

all_stats = {}


async def serv_stat(websocket, path):
    while True:
        # Path('/tmp/STAT').read_text()
        await websocket.send(json.dumps(all_stats))
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()
loop.run_until_complete(
    websockets.serve(serv_stat, "0.0.0.0", 1720, ping_interval=5, ping_timeout=10)
)

routes = web.RouteTableDef()


@routes.post("/")
async def hello(request):
    res_body = await request.json()
    all_stats[request.remote] = res_body
    # import IPython; IPython.embed()
    return web.Response(text="OK")


app = web.Application()
app.add_routes(routes)
web.run_app(app)

loop.run_forever()
