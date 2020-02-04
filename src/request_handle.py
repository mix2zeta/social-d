import csv
import redis
import rq
from aiohttp import web
import json

import arrow
from conf import settings
from worker.csv_handle import split_spawn_file_api

from database import DBConnection

async def poke_task(request: web.BaseRequest) -> web.json_response:
    with rq.Connection(redis.from_url(settings.REDIS_URL)):
        q = rq.Queue()
        task = q.enqueue(split_spawn_file_api, 'raw_data/rawdata.csv')

        return web.json_response({'task': task.get_id()})


async def get_task(request: web.BaseRequest) -> web.json_response:
    with rq.Connection(redis.from_url(settings.REDIS_URL)):
        q = rq.Queue()
        task = q.fetch_job(request.match_info.get('task_id'))

        return web.json_response({
            "task_id": task.get_id(),
            "task_status": task.get_status(),
            "task_result": task.result,
        })


async def get_daily_message_count(request: web.BaseRequest) -> web.json_response:
    from_date = request.match_info.get('from')
    to_date = request.match_info.get('to')

    async with DBConnection(request) as connection, connection.transaction(isolation='serializable'):
        result = await connection.fetch("""
            SELECT to_char(date_trunc('day', time), 'YYYY-MM-DD') as date, count(*) 
            FROM data 
            WHERE time BETWEEN $1 AND $2 
            GROUP BY date 
            ORDER BY date ASC
        """,
            arrow.get(from_date).datetime,
            arrow.get(to_date).datetime
        )
        return web.json_response(dict(result))


async def get_account_by_message(request: web.BaseRequest) -> web.json_response:
    from_date = request.match_info.get('from')
    to_date = request.match_info.get('to')

    and_list = ['samsung', 's10']
    or_list = ['@Chuuchu69 เปนกำลังใจให้รายเดือนเหมือนกันค่ะ']

    sub_query = ''
    for value in and_list:
        sub_query += f" AND message like '%{value}%'"
    for value in or_list:
        sub_query += f" OR message like '%{value}%'"

    async with DBConnection(request) as connection, connection.transaction(isolation='serializable'): # still not correct , distrint and get account
        query = f"""
            SELECT channel, owner_id, owner_name, message
            FROM data 
            WHERE time BETWEEN $1 AND $2 
            {sub_query}
            ORDER BY 2,3,4
        """
        print(query)
        result = await connection.fetch(query,
            arrow.get(from_date).datetime,
            arrow.get(to_date).datetime,
        )
        payload = []
        for item in result:
            payload.append(dict(item))
        return web.json_response(payload)



async def get_message_by_engagement(request: web.BaseRequest) -> web.json_response:
    from_date = request.match_info.get('from')
    to_date = request.match_info.get('to')

    async with DBConnection(request) as connection, connection.transaction(isolation='serializable'):
        result = await connection.fetch("""
            SELECT engagement, time::TEXT, message
            FROM data 
            WHERE time BETWEEN $1 AND $2 
            ORDER BY engagement DESC 
            limit 10
        """,
            arrow.get(from_date).datetime,
            arrow.get(to_date).datetime
        )
        payload = []
        for item in result:
            payload.append(dict(item))
        return web.json_response(payload)


from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

async def get_word_cloud(request: web.FileResponse) -> web.json_response:
    dictionary = {
        'asdasdA': 1,
        'fefegb': 5,
        'Cdsgsdg': 7,
        'Dweeeeeeeeeeee': 80
    }

    # wc = WordCloud(background_color="white",width=1000,height=1000, max_words=100,relative_scaling=0.5,normalize_plurals=False)
    wc = WordCloud(background_color="white",width=1000,height=1000, max_words=100)
    wc.generate_from_frequencies(dictionary)
    plt.imshow(wc)
    # plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.savefig("media/spa_wine.jpg", format="jpg")
    return web.FileResponse('media/spa_wine.jpg')

async def get_hash_tag_cloud(request: web.BaseRequest) -> web.json_response:
    pass