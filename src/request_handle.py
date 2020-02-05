import csv
import redis
import rq
from aiohttp import web
import json

import arrow
from conf import settings
from worker.csv_handle import split_spawn_file_api
from router import reverse
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


async def get_message_by_id(request: web.BaseRequest) -> web.json_response:
    msg_id = request.match_info.get('msg_id')

    async with DBConnection(request) as connection, connection.transaction(isolation='serializable'):
        result = await connection.fetchrow("""
            SELECT * 
            FROM data 
            WHERE id = $1
        """,
            msg_id,
        )
        payload = dict(result)
        payload['time'] = payload['time'].isoformat()
        return web.json_response(payload)


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
    key_word = request.query.get('q').split(' ')

    and_list = []
    or_list = []

    and_list.append(key_word.pop(0))
    index = 0
    for _ in range(0, int(len(key_word)/2)):
        if key_word[index].lower() == 'and':
            and_list.append(key_word[index+1])
        if key_word[index].lower() == 'or':
            or_list.append(key_word[index+1])
        index += 2

    sub_query = ''
    for value in and_list:
        sub_query += f" AND lower(message) like '%{value.lower()}%'"
    for value in or_list:
        sub_query += f" OR lower(message) like '%{value.lower()}%'"

    async with DBConnection(request) as connection, connection.transaction(isolation='serializable'):
        query = f"""
            SELECT owner_id, owner_name, sum(engagement) as total_engagement, array_agg(id) as id_list
            FROM data 
            WHERE time BETWEEN $1 AND $2 
            {sub_query}
            GROUP BY owner_id,owner_name
            ORDER BY total_engagement DESC
            limit 10
        """
        print(query)
        result = await connection.fetch(query,
            arrow.get(from_date).datetime,
            arrow.get(to_date).datetime,
        )
        payload = []
        for item in result:
            item = dict(item)
            url_id_list = []
            for msg in item['id_list']:
                msg = reverse('message', msg_id=msg)
                url_id_list.append(msg)
            item['id_list'] = url_id_list
            payload.append(item)
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