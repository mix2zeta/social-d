import csv
import redis
import rq
from aiohttp import web

from conf import settings

async def redeem_product(request):
    # raise web.HTTPNotFound(text='Member number not found: please link with the1 account')
    from fix_csv import split_spawn_file_api

    with rq.Connection(redis.from_url(settings.REDIS_URL)):
        q = rq.Queue()
        task = q.enqueue(split_spawn_file_api, 'raw_data/rawdata.csv')

        return web.json_response({'foo': task.get_id()})


async def get_task(request):
    with rq.Connection(redis.from_url(settings.REDIS_URL)):
        q = rq.Queue()
        task = q.fetch_job(request.match_info.get('task_id'))

        return web.json_response({
            "task_id": task.get_id(),
            "task_status": task.get_status(),
            "task_result": task.result,
        })
