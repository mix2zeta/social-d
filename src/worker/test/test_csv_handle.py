import hashlib
import asyncio

import pytest
from aiohttp.test_utils import unittest_run_loop

from conf import settings
from tests import BaseTestCase
from worker import csv_handle


class Test(BaseTestCase):
    async def setUpAsync(self):
        await super().setUpAsync()
        settings.RAW_DATA_PATH = 'worker/test/test_raw_data'
        settings.SPLIT_DATA_PATH = 'worker/test/test_split_data'
        settings.CSV_LINE_LIMIT = 50


    @unittest_run_loop
    async def test_check_is_any_new_file(self):
        csv_handle.check_is_any_new_file()


    @unittest_run_loop
    @pytest.mark.filterwarnings('ignore:\'U\' mode is deprecated')
    async def test_split_spawn_file_api(self):
        file_path = f'{settings.RAW_DATA_PATH}/raw_100.csv'
        file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
        expect = ['worker/test/test_split_data/raw_100__1.csv', 'worker/test/test_split_data/raw_100__2.csv']
        actual = await csv_handle.split_spawn_file(file_path)
        assert expect == actual
        record = await self.connection.fetch("SELECT * FROM file WHERE hash=$1", file_hash)
        assert len(record) == 2


    @unittest_run_loop
    @pytest.mark.filterwarnings('ignore:\'U\' mode is deprecated')
    async def test_insert_data_from_csv(self):
        file_path = f'{settings.RAW_DATA_PATH}/raw_10.csv'
        await csv_handle.insert_data_from_csv(file_path, 'file_hash')

        record = await self.connection.fetch("SELECT * FROM data")
        assert len(record) == 6


    @unittest_run_loop
    @pytest.mark.filterwarnings('ignore:\'U\' mode is deprecated')
    async def test_get_line_from_csv(self):
        expect = [
            ['1079784244640010240', 'tweet', 'จุดพลุกันสนุกมากนะ', '2019-01-01 00:00:00', '9672', 'twitter', '1013618778', '💖'],
            ['1079784245067829254', 'tweet', 'Happy New Years 2019🎉🎉 นะคะทุกคน ปีนี้ก็ขอฝากตัวด้วยค่ะ!ปีที่แล้วถ้าทำอะไรผิดพลาดหรือทำให้ไม่พอใจอะไรไปต้องขอโทษด้วยนะคะ🙏ดีใจที่ได้รู้จักกับทุกคนค่ะ แล้วก็ขอบคุณที่มาเวิ่นเว้อด้วยกันนะคะ ดีใจมากเลย', '2019-01-01 00:00:00', '9857', 'twitter', '2161099140', '🎄FreSan☕59 days countdown to wmtsb3'],
            ['1079784244979744768', 'reply', '@exseongwuxjrs วับรุ่นเลย', '2019-01-01 00:00:00', '866', 'twitter', '915388710752985088', 'madclownhub'],
            ['1079784245474676743', 'tweet', '백현 give me your 💛💛💛💛💛', '2019-01-01 00:00:00', '7287', 'twitter', '251466504', 'lb ft.loveshot 💎'],
            ['1079784246317768705', 'tweet', 'สวัสดีปีหม่ายยยยยยย', '2019-01-01 00:00:00', '1774', 'twitter', '433258245', "▲'ฟัคทองกำลังทำทีสิส;}"],
            ['1079784246720352256', 'reply', '@quexnmxe เป็นแฟนกับพี่นะครับเด็กดีสัญญาว่าจะรักษาหนูไว้ให้นานที่สุดเท่าที่จะทำได้นะ', '2019-01-01 00:00:00', '495', 'twitter', '1079574135720689664', '𝓿𝓲𝓷𝓽𝓪𝓰𝓮🍳'],
            [],
            ]
        actual = []
        for row in csv_handle.get_line_from_csv(f'{settings.RAW_DATA_PATH}/raw_10.csv'):
            actual.append(row)
        assert expect == actual
