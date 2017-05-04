import time
from concurrent.futures import ThreadPoolExecutor
import requests
import aiohttp
import asyncio
NUMBERS = range(12)
url = 'http://httpbin.org/get?a={}'

async def fetch(a):
    async with aiohttp.request('GET',url.format(a)) as r:
        data = await r.json()
        return data['args']['a']

start = time.time()
event_loop = asyncio.get_event_loop()
tasks = [fetch(num) for num in NUMBERS]
results = event_loop.run_until_complete(asyncio.gather(*tasks))
for num, result in zip(NUMBERS,results):
    print('fetch({}) = {}'.format(num, result))

print('Use asyncio+aiohttp cost: {}'.format(time.time() - start))