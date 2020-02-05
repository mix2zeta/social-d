import os

from aiohttp.test_utils import unittest_run_loop

from conf import settings
from tests import BaseTestCase


class RequestIntegrationTest(BaseTestCase):
    async def setUpAsync(self):
        await super().setUpAsync()
        await self.connection.execute("""
            INSERT INTO data (id, type, message, time, engagement, channel, owner_id, owner_name)
            VALUES
                ('1079784244640010240','tweet','จุดพลุกันสนุกมากนะ #test','2019-01-01 00:00:00',9672,'twitter','1013618778','💖'),
                ('1079784245067829254','tweet','Happy New Years 2019🎉🎉 นะคะทุกคน ปีนี้ก็ขอฝากตัวด้วยค่ะ!ปีที่แล้วถ้าทำอะไรผิดพลาดหรือทำให้ไม่พอใจอะไรไปต้องขอโทษด้วยนะคะ🙏ดีใจที่ได้รู้จักกับทุกคนค่ะ แล้วก็ขอบคุณที่มาเวิ่นเว้อด้วยกันนะคะ ดีใจมากเลย','2019-01-01 00:00:00',9857,'twitter','2161099140','🎄FreSan☕59 days countdown to wmtsb3'),
                ('1079784244979744768','reply','@exseongwuxjrs วับรุ่นเลย #TEEN','2019-01-01 00:00:00',866,'twitter','915388710752985088','madclownhub'),
                ('1079784245474676743','tweet','백현 give me your 💛💛💛💛💛','2019-01-01 00:00:00',7287,'twitter','251466504','lb ft.loveshot 💎'),
                ('1079784246317768705','tweet','สวัสดีปีหม่ายยยยยยย #test','2019-01-02 00:00:00',1774,'twitter','433258245','ฟัคทองกำลังทำทีสิส;}'),
                ('1079784246720352256','reply','@quexnmxe เป็นแฟนกับพี่นะครับเด็กดีสัญญาว่าจะรักษาหนูไว้ให้นานที่สุดเท่าที่จะทำได้นะ','2019-01-03 00:00:00',495,'twitter','1079574135720689664','𝓿𝓲𝓷𝓽𝓪𝓰𝓮🍳')
        """)

        self.from_date = '2019-01-01'
        self.to_date = '2019-01-03'


    @unittest_run_loop
    async def test_poke_200(self):
        response = await self.client.get(f'/poke')
        self.assertEqual(response.status, 200) 


    @unittest_run_loop
    async def test_get_message_by_id_200(self):
        msg_id = '1079784244640010240'
        response = await self.client.get(f'/message/{msg_id}')
        self.assertEqual(response.status, 200) 
        actual = await response.json()
        self.assertEqual(actual['message'], 'จุดพลุกันสนุกมากนะ #test') 


    @unittest_run_loop
    async def test_get_message_by_id_404(self):
        msg_id = 'not_exist_id'
        response = await self.client.get(f'/message/{msg_id}')
        self.assertEqual(response.status, 404) 


    @unittest_run_loop
    async def test_get_daily_message_count_200(self):
        expect = {'2019-01-01': 4, '2019-01-02': 1, '2019-01-03': 1}

        response = await self.client.get(f'/date/{self.from_date}/{self.to_date}/message/daily')
        self.assertEqual(response.status, 200) 
        actual = await response.json()
        self.assertEqual(actual, expect) 


    @unittest_run_loop
    async def test_get_daily_message_count_404(self):
        from_date = '2012-01-01'
        to_date = '2012-01-03'

        response = await self.client.get(f'/date/{from_date}/{to_date}/message/daily')
        self.assertEqual(response.status, 404)


    @unittest_run_loop
    async def test_get_account_by_message_200(self):
        expect = [
            {'owner_id': '2161099140', 'owner_name': '🎄FreSan☕59 days countdown to wmtsb3', 'total_engagement': 9857, 'id_list': ['http://localhost:1111/message/1079784245067829254']}, 
            {'owner_id': '433258245', 'owner_name': 'ฟัคทองกำลังทำทีสิส;}', 'total_engagement': 1774, 'id_list': ['http://localhost:1111/message/1079784246317768705']}
        ]

        response = await self.client.get(f'/date/{self.from_date}/{self.to_date}/message/top?q=ปี')
        self.assertEqual(response.status, 200) 
        actual = await response.json()
        self.assertEqual(actual, expect) 


    @unittest_run_loop
    async def test_get_account_by_message_200_and_or(self):
        expect = [
            {'owner_id': '2161099140', 'owner_name': '🎄FreSan☕59 days countdown to wmtsb3', 'total_engagement': 9857, 'id_list': ['http://localhost:1111/message/1079784245067829254']}, 
            {'owner_id': '251466504', 'owner_name': 'lb ft.loveshot 💎', 'total_engagement': 7287, 'id_list': ['http://localhost:1111/message/1079784245474676743']}
        ]

        response = await self.client.get(f'/date/{self.from_date}/{self.to_date}/message/top?q=ปี AND แล้ว OR give')
        self.assertEqual(response.status, 200) 
        actual = await response.json()
        self.assertEqual(actual, expect) 


    @unittest_run_loop
    async def test_get_account_by_message_404(self):
        from_date = '1990-01-01'
        to_date = '1990-02-02'
        response = await self.client.get(f'/date/{from_date}/{to_date}/message/top?q=ไม่น่าจะมีคำนี้')
        self.assertEqual(response.status, 404)


    @unittest_run_loop
    async def test_get_message_by_engagement_200(self):
        response = await self.client.get(f'/date/{self.from_date}/{self.to_date}/message/engagement')
        self.assertEqual(response.status, 200) 
        actual = await response.json()
        self.assertEqual(actual[0]['engagement'], 9857) 


    @unittest_run_loop
    async def test_get_message_by_engagement_404(self):
        from_date = '1990-01-01'
        to_date = '1990-02-02'
        response = await self.client.get(f'/date/{from_date}/{to_date}/message/engagement')
        self.assertEqual(response.status, 404)


    @unittest_run_loop
    async def test_get_word_cloud_200(self):
        response = await self.client.get(f'/date/{self.from_date}/{self.to_date}/message/wordcloud')
        self.assertEqual(response.status, 200)
        self.assertEqual(os.path.exists(f"{settings.MEDIA_PATH}/wordcloud__{self.from_date}__{self.to_date}.png"), True)


    @unittest_run_loop
    async def test_get_word_cloud_404(self):
        from_date = '1990-01-01'
        to_date = '1990-02-02'
        response = await self.client.get(f'/date/{from_date}/{to_date}/message/wordcloud')
        self.assertEqual(response.status, 404) 


    @unittest_run_loop
    async def test_get_word_cloud_200_cache(self):
        response = await self.client.get(f'/date/{self.from_date}/{self.to_date}/message/word')
        self.assertEqual(response.status, 200) 


    @unittest_run_loop
    async def test_get_hashtag_cloud_200(self):
        response = await self.client.get(f'/date/{self.from_date}/{self.to_date}/message/hashtag')
        self.assertEqual(response.status, 200) 
        self.assertEqual(os.path.exists(f"{settings.MEDIA_PATH}/hashtag__{self.from_date}__{self.to_date}.png"), True)


    @unittest_run_loop
    async def test_get_mention_cloud_200(self):
        response = await self.client.get(f'/date/{self.from_date}/{self.to_date}/message/mention')
        self.assertEqual(response.status, 200) 
        self.assertEqual(os.path.exists(f"{settings.MEDIA_PATH}/mention__{self.from_date}__{self.to_date}.png"), True)
