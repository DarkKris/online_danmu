import websockets
import asyncio
import threading
import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


wss = []
domain_name = ''


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global wss
        req_body = self.rfile.read(int(self.headers['content-length']))
        try:
            obj = json.loads(req_body.decode("utf-8"))
        except Exception as e:
            obj = dict()
        print(obj)
        content: str = obj.get("content", "")
        print(content)
        for ws in wss:
            try:
                await ws.send(content)
            except Exception as e:
                print(e)
        self.Response("")

    def _send_cors_headers(self):
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")

    def Response(self, body):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(body.encode())


async def ws_register(ws: websockets.WebSocketClientProtocol, path):
    wss.append(ws)
    print(ws, path)
    while True:
        try:
            recv_text = await ws.recv()
        except:
            pass


def run_serve():
    global domain_name
    port = 6721
    server_address = (domain_name, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print('server running...')
    httpd.serve_forever()


def run_wsr():
    global domain_name
    port = 9988
    server = websockets.serve(ws_register, domain_name, port)
    print('websocket running...')
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()


class ServeThread(threading.Thread):
    def run(self):
        run_serve()


if __name__ == "__main__":
    serve_thread = ServeThread()
    serve_thread.start()
    run_wsr()
