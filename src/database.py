from conf import settings
import asyncpg
import json


async def get_connection():
    cnx = await asyncpg.connect(
        host=settings.DATABASE.PGHOST,
        database=settings.DATABASE.PGDBNAME,
        user=settings.DATABASE.PGUSER,
        password=settings.DATABASE.PGPASSWORD,
        port=settings.DATABASE.PGPORT
    )
    await cnx.set_type_codec("jsonb", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")
    await cnx.set_type_codec("json", encoder=json.dumps, decoder=json.loads, schema="pg_catalog")
    return cnx
    

class DBConnection():
    def __init__(self, request):
        self.request = request
        self.pool = request.app['pool']

    async def __aenter__(self):
        self.connection = await self.pool.acquire()
        return self.connection

    async def __aexit__(self, exc_type, exc, tb):
        await self.pool.release(self.connection)
