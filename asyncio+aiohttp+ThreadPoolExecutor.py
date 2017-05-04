import time
from concurrent.futures import ThreadPoolExecutor
import requests
import aiohttp
import asyncio
import math
NUMBERS = range(12)
url = 'http://httpbin.org/get?a={}'

async def fetch_async(a):
    async with aiohttp.request('GET',url.format(a)) as r:
        data = await r.json()
        return a,data['args']['a']

start = time.time()

def sub_loop(numbers):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [fetch_async(num) for num in numbers]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    for num, result in results:
        print('fetch({}) = {}'.format(num, result))

async def run(executor, numbers):
    await asyncio.get_event_loop().run_in_executor(executor,sub_loop,numbers)

def chunks(l, size):
    n = math.ceil(len(l) / size)
    for i in range(0, len(l), n):
        yield l[i:i + n]        

event_loop = asyncio.get_event_loop()
executor = ThreadPoolExecutor(4)
tasks = [run(executor, chunked) for chunked in chunks(NUMBERS, 3)]
results = event_loop.run_until_complete(asyncio.gather(*tasks))
print('Use asyncio+aiohttp+ThreadPoolExecutor cost: {}'.format(time.time() - start))
