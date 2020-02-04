import csv
import redis
import rq
from aiohttp import web

from conf import settings
from worker.csv_handle import split_spawn_file_api

async def poke_task(request):
    with rq.Connection(redis.from_url(settings.REDIS_URL)):
        q = rq.Queue()
        task = q.enqueue(split_spawn_file_api, 'raw_data/rawdata.csv')

        return web.json_response({'task': task.get_id()})


async def get_task(request):
    with rq.Connection(redis.from_url(settings.REDIS_URL)):
        q = rq.Queue()
        task = q.fetch_job(request.match_info.get('task_id'))

        return web.json_response({
            "task_id": task.get_id(),
            "task_status": task.get_status(),
            "task_result": task.result,
        })


async def get_daily_message_count(request):
    pass

async def get_account_by_message(request):
    pass

async def get_message_by_engagement(request):
    pass


from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

async def get_word_cloud(request):
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
    plt.savefig("spa_wine.jpg", format="jpg")
    return web.FileResponse('spa_wine.jpg')

async def get_hash_tag_cloud(request):
    pass