from aiohttp.test_utils import unittest_run_loop

from tests import BaseTestCase

class GetContractUnitTest(BaseTestCase):
    async def setUpAsync(self):
        await super().setUpAsync()

    @unittest_run_loop
    async def test_return_non_exist_contract_token(self):
        response = await self.client.put(f'/account')