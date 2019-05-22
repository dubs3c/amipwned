import asyncio
import logging
import re
import sys

from psycopg2 import OperationalError
from aiohttp import web
import asyncpg
from amipwned.config import Config

routes = web.RouteTableDef()
logging.basicConfig(level=logging.INFO, format="%(levelname)7s: %(message)s")
LOG = logging.getLogger("amipwned")
LOG.setLevel(logging.INFO)


@routes.get("/")
async def hello(request):
    return web.Response(text="am i pwned?")


@routes.get("/hash/{hash}")
async def check_hash(request):
    hash = request.match_info["hash"]
    pool = request.app["pgsql"]
    async with pool.acquire() as conn:
        async with conn.transaction():
            found = await conn.fetchval("SELECT hash FROM dump WHERE hash = $1", hash)

            if found:
                return web.json_response({"status": "You have been pwned"})
            else:
                return web.json_response(
                    {"status": "Does not look like you have been pwned"}, status=404
                )


async def get_app():
    async def close_pgsql(aspp):
        LOG.debug("Closing Postgresql connection...")
        await app["pgsql"].close()

    app = web.Application()
    conf = Config()
    db = conf.database()
    try:
        app["pgsql"] = await asyncpg.create_pool(
            user=db.get("username"),
            host=db.get("host"),
            password=db.get("password"),
            port=db.get("port"),
            database=db.get("name"),
            command_timeout=60,
        )
    except OperationalError as e:
        print(f"[-] Error connecting to DB: {e}")
        sys.exit(1)
    app.add_routes(routes)
    app.on_shutdown.append(close_pgsql)

    return app


#loop = asyncio.get_event_loop()
#app = loop.run_until_complete(get_app())
#web.run_app(app, port=8000)
