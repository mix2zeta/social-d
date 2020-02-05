import asyncpg
import asyncio
import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from conf import settings
from server import create_app


class BaseTestCase(AioHTTPTestCase):
    async def get_application(self):
        return await create_app()
        

    async def setUpAsync(self):
        self.connection = await self.app["pool"].acquire()
        settings.MEDIA_PATH = '/usr/src/tests/test_media'


    async def tearDownAsync(self):
        await self.connection.execute('''
            TRUNCATE TABLE file, data CASCADE
        ''')
        await self.connection.close()