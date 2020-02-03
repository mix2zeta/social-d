from aiohttp import web

async def redeem_product(request):
    return web.json_response({'foo': 'bar'})