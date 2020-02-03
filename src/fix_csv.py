import csv
import arrow 
from database import get_connection
import asyncio
import hashlib


def aasync_ja(file_path):
    return asyncio.run(tmp_ja('raw_data/rawdata.csv'))

async def tmp_ja(file_path):
    file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
    connection = await get_connection()
    async with connection.transaction():
        # await connection.execute("INSERT INTO file VALUES ($1, $2)", file_path, file_hash)

        count = 0
        for value in read_csv(file_path):
            count += 1
            print(count)
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
            except:
                pass
        return count 

def read_csv(file_path):
    with open(file_path, 'rU') as csv_file:
        csv.field_size_limit(531072) # 0.5mb per field
        spamreader = csv.reader((line.replace('\0','') for line in csv_file), delimiter=",", dialect=csv.excel_tab)
        next(spamreader, None) # skip header
        new_line = []
        aaa = 1
        for row in spamreader:
            # print(aaa)
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
                    # int(value[4])
                except:
                    for var in new_line[3:]:
                        new_line[2] = new_line[2] + new_line[3]
                        new_line.pop(3)
                    continue

                if new_line[1] not in ('tweet','reply','comment','reply-comment','post'):
                    new_line = []
                    continue
                    # import ipdb; ipdb.set_trace()
                    # for var in new_line[3:]:
                    #     new_line[2] = new_line[2] + new_line[3]
                    #     new_line.pop(3)
                    # continue

                # try:
                #     int(value[4])
                # except:
                #     new_line = []
                #     continue


                aaa += 1
                yield new_line
                new_line = []


            if len(new_line) > 8:
                raise ValueError('this logix is not work')


# count = 0
# for value in read_csv('raw_data/rawdata.csv'):
#     count += 1
    # if count >= 33778:
    #     print(value)
    # print(count)