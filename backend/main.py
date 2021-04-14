import websockets
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


wss = []


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global websockets
        req_body = self.rfile.read(int(self.headers['content-length']))
        obj = json.loads(req_body.decode("utf-8"))
        print(req_body)
        content: str = req_body.get("content", "")
        for ws in wss:
            ws.send(content)


async def ws_register(ws, path):
    global websockets
    wss.append(ws)
    print(ws, path)


def run_serve():
    port = 6721
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print('server running...')
    httpd.serve_forever()


def run_wsr():
    port = 9988
    server = websockets.serve(ws_register, '', port)
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
