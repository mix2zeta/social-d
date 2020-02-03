import os
from conf import settings
import asyncio
import logging

import asyncpg
from aiohttp import web
from router import generate_routes
# from middlewares import exception
import simplejson
import sys


async def init_cnx(cnx):
    await cnx.set_type_codec("jsonb", encoder=simplejson.dumps, decoder=simplejson.loads, schema="pg_catalog")
    await cnx.set_type_codec("json", encoder=simplejson.dumps, decoder=simplejson.loads, schema="pg_catalog")
    return cnx


async def create_app():
    """Initialize the application server."""
    # log = logging.getLogger()
    # app = web.Application(middlewares=[exception.handle_exception], logger=log)
    app = web.Application(logger=log)
    # Create a database connection pool
    app["pool"] = await asyncpg.create_pool(
        host=settings.DATABASE.PGHOST,
        database=settings.DATABASE.PGDBNAME,
        user=settings.DATABASE.PGUSER,
        password=settings.DATABASE.PGPASSWORD,
        port=settings.DATABASE.PGPORT,
        init=init_cnx,
    )
    app.add_routes(generate_routes())
    app.on_shutdown.append(on_shutdown)
    return app


async def on_shutdown(app):
    logging.info("Shutting down...")
    await app["pool"].close() # Close all database connections
    logging.info("Connection pool: Closed")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(create_app())
    logging.basicConfig(
        stream=sys.stderr,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        level=settings.APP.LOGLEVEL,
        datefmt="[%Y-%m-%dT%H:%M:%S%z]",
    )
    web.run_app(
        app,
        host=settings.APP.HOST,
        port=settings.APP.PORT,
        access_log_format='%a "%r" %s %b "%{Referer}i" "%{Fost-Request-ID}i" "%{X-Real-IP}i" "%{User-Agent}i" %Tfs.',
        # [2019-11-06T05:50:00+0000] 172.18.0.1 "GET /account/B HTTP/1.1" 404 172 "-" "-" "-" "PostmanRuntime/7.19.0" 0.002807s.
    )
