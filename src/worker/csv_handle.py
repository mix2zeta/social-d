import asyncio
import csv
import os
from worker.csv_splitter import split

import arrow 
import hashlib
import redis
import rq

from conf import settings
from database import get_connection


def check_is_any_new_file():
    for csv_file in os.listdir(settings.RAW_DATA_PATH):
        if csv_file[-4:] == '.csv':
            with rq.Connection(redis.from_url(settings.REDIS_URL)):
                q = rq.Queue()
                task = q.enqueue(split_spawn_file_api, f'{settings.RAW_DATA_PATH}/{csv_file}')


def split_spawn_file_api(file_path):
    return asyncio.run(split_spawn_file(file_path))

async def split_spawn_file(file_path):
    output = []
    connection = await get_connection()
    async with connection.transaction(isolation='serializable'):
        file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

        check_hash = await connection.fetch("SELECT * FROM file WHERE hash=$1", file_hash)
        if check_hash != []:
            print('already process')
            return None # already process

        template = f'{os.path.basename(file_path).replace(".csv", "")}__%s.csv'
        output = split(open(file_path, 'rU'), row_limit=settings.CSV_LINE_LIMIT, output_path=settings.SPLIT_DATA_PATH, output_name_template=template)

        for item in output:
            with rq.Connection(redis.from_url(settings.REDIS_URL)):
                q = rq.Queue()
                task = q.enqueue(insert_data_from_csv_api, item, file_hash)

                await connection.execute("""
                    INSERT INTO file ("name", "hash", "split", "task_id") 
                    VALUES ($1, $2, $3, $4)
                """, file_path, file_hash, item, task.get_id())
        
    await connection.close()
    print(output)
    return output


def insert_data_from_csv_api(file_path, file_hash):
    return asyncio.run(insert_data_from_csv(file_path, file_hash))

async def insert_data_from_csv(file_path, file_hash):
    count = 0
    connection = await get_connection()
    async with connection.transaction(isolation='serializable'):
        for value in get_line_from_csv(file_path):
            count += 1
            try:
                value[3] = arrow.get(value[3]).datetime
                value[4] = int(value[4])
                await connection.execute("""
                    INSERT INTO data (id, type, message, time, engagement, channel, owner_id, owner_name)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (id) 
                    DO NOTHING
                """,
                    *value
                )
            except: # at this point I accept that I can't prase all data... just record error
                await connection.execute("""
                    INSERT INTO data_error (data, from_file)
                    VALUES ($1, $2)
                """,
                    str(value),
                    file_path
                )
        await connection.execute("UPDATE file SET executed=now() WHERE hash=$1 AND split=$2", file_hash, file_path)

    await connection.close()
    return count 


def get_line_from_csv(file_path):
    with open(file_path, 'rU') as csv_file:
        csv.field_size_limit(531072) # 0.5mb per field
        spamreader = csv.reader((line.replace('\0','') for line in csv_file), delimiter=",", dialect=csv.excel_tab) # we need rU but remove null byte
        next(spamreader, None) # skip header
        new_line = []
        aaa = 1
        for row in spamreader:
            l_index = len(new_line)

            if len(row) == 0:
                continue

            if l_index == 0:
                new_line = new_line + row
            elif 8 > l_index > 0:
                new_line[l_index-1] = new_line[l_index-1] + row[0]
                new_line = new_line + row[1:]

            if len(new_line) > 8:
                for var in new_line[3:]:
                    try:
                        arrow.get(var)
                        break
                    except:
                        new_line[2] = new_line[2] + new_line[3]
                        new_line.pop(3)

            if len(new_line) > 8:
                for var in new_line[8:]:
                        new_line[7] = new_line[7] + new_line[8]
                        new_line.pop(8)
                            
            if len(new_line) == 8:
                try:
                    arrow.get(new_line[3])
                except:
                    for var in new_line[3:]:
                        new_line[2] = new_line[2] + new_line[3]
                        new_line.pop(3)
                    continue

                aaa += 1
                yield new_line
                new_line = []

            if len(new_line) > 8:
                raise ValueError('This logic is not work')

        yield new_line # return last line for error
