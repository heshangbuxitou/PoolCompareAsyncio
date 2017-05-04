import time
from concurrent.futures import ThreadPoolExecutor
import requests
import asyncio
NUMBERS = range(12)
url = 'http://httpbin.org/get?a={}'

def fetch(a):
    r = requests.get(url.format(a))
    return r.json()['args']['a']
start = time.time()

async def run_scraper_tasks(executor):
    loop = asyncio.get_event_loop()

    blocking_tasks = []
    for num in NUMBERS:
        task = loop.run_in_executor(executor, fetch, num)
        task.__num = num
        blocking_tasks.append(task)
    completed, pending = await asyncio.wait(blocking_tasks)
    results = {t.__num:t.result() for t in completed}
    for num, result in sorted(results.items(),key=lambda x:x[0]):
        print('fetch({}) = {}'.format(num, result))

start = time.time()
executor = ThreadPoolExecutor(max_workers=4)
event_loop = asyncio.get_event_loop()

event_loop.run_until_complete(
    run_scraper_tasks(executor)
)

print('Use asyncio+requests+ThreadPoolExecutor cost: {}'.format(time.time() - start))
