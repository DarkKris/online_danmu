import requests
import time
from concurrent.futures import ThreadPoolExecutor

res = []

def post_test():
    global res
    url = 'http://localhost:6721'
    res.append(requests.post(url, data={
        "content": "hello world",
    }))

def main():
    global res
    exe = ThreadPoolExecutor(max_workers=30)
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