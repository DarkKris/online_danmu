import requests
import time
import json
from typing import List
from concurrent.futures import ThreadPoolExecutor

res = []

def append_head_tail(lst_unicodes) -> List[str]:
    utf8_bytes = bytes()
    for unicode_char in lst_unicodes:
        utf8_bytes += unicode_char.encode('utf-8')
    return utf8_bytes


def post_test():
    global res
    url = 'http://danmu.deanti.wang/api'
    string = bytes()
    for letter in 'hhhhhh':
        string += letter.encode('utf-8')
        head_tail = append_head_tail(['\u0326'] * 16)
        string += head_tail
    try:
        res.append(requests.post(url, data=json.dumps({
            "content": string.decode('utf-8'),
            "nick": "hhh",
        }).encode('utf-8')))
    except Exception as e:
        print(e)


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
