import os
from datetime import datetime, timedelta

import redis
import rq
from rq_scheduler import Scheduler

from conf import settings
from worker.csv_handle import check_is_any_new_file

def loop_check_is_any_new_file():
    with rq.Connection(redis.from_url(settings.REDIS_URL)):
        q = rq.Queue()
        scheduler = Scheduler(queue=q)
        scheduler.schedule(
            scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
            func=check_is_any_new_file,
            interval=600,                   # Time before the function is called again, in seconds
        )
