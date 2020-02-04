import asyncio
import logging
import json
import os
import sys

import asyncpg
from aiohttp import web

from conf import settings
from router import generate_routes


async def init_cnx(cnx):
    await cnx.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")
    await cnx.set_type_codec("json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")
    return cnx


async def create_app():
    """Initialize the application server."""
    app = web.Application()
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
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, host="0.0.0.0", port=80)
