import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor

res = []

def post_test():
    global res
    url = 'http://danmu.deanti.wang/api'
    res.append(requests.post(url, data=json.dumps({
        "content": "hello world",
    })))

def main():
    global res
    exe = ThreadPoolExecutor(max_workers=100)
    times = 1000
    for i in range(times):
        exe.submit(post_test)
    while len(res) < times:
        time.sleep(0.3)
    for rsp in res:
        if rsp.status_code != 200:
            print(rsp.status_code)

if __name__ == '__main__':
    main()