import asyncpg
import asyncio
import simplejson
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from conf import settings
from server import create_app

async def init_cnx(cnx):
    await cnx.set_type_codec("jsonb", encoder=simplejson.dumps, decoder=simplejson.loads, schema="pg_catalog")
    await cnx.set_type_codec("json", encoder=simplejson.dumps, decoder=simplejson.loads, schema="pg_catalog")
    return cnx

class BaseTestCase(AioHTTPTestCase):
    async def get_application(self):
        return await create_app()


    async def setUpAsync(self):
        # self.loop = asyncio.get_event_loop()

        self.connection = await asyncpg.create_pool(
            host=settings.DATABASE.PGHOST,
            database=settings.DATABASE.PGDBNAME,
            user=settings.DATABASE.PGUSER,
            password=settings.DATABASE.PGPASSWORD,
            port=settings.DATABASE.PGPORT,
            init=init_cnx,
        )

        self.connection = await self.connection.acquire()

    async def tearDownAsync(self):
        await self.connection.execute('''
            TRUNCATE TABLE file, data CASCADE
        ''')
        await self.connection.close()
        connection_pool = self.app['pool']
        await connection_pool.close()