from aiohttp import web
import csv

async def redeem_product(request):
    raise web.HTTPNotFound(text='Member number not found: please link with the1 account')
    return web.json_response({'foo': 'bar'})


def read_csv():

    with open('raw_data/raw_10.csv', newline='\n') as csv_file:
        spamreader = csv.reader(csv_file)
        for row in spamreader:
            import ipdb; ipdb.set_trace()
            print(', '.join(row))
    print('Hi')

# import asyncio
# asyncio.run(read_csv())

read_csv()