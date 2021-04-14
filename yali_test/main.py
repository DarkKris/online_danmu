import requests
import time
from concurrent.futures import ThreadPoolExecutor

res = []

def post_test():
    global res
    url = 'http://baidu.com'
    res.append(requests.post(url, data={}))


exe = ThreadPoolExecutor(max_workers=10)

times = 100

for i in range(times):
    exe.submit(post_test)

while len(res) < times:
    pass

for i in res:
    print(i)
