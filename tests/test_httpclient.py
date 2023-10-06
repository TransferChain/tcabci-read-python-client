import unittest
import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from tcabci_read_client import HttpClient


class DummyHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        print(self.path)
        if self.path == '/v1/tx_search/p':
            pass
        elif self.path == '/v1/broadcast':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"data":
                        {
                            "hash": "E08F7AD",
                            "code": 0,
                            "data": "",
                            "log": "",
                            "codespace": ""},
                        "total_count": 0,
                        "error": True,
                        "errors": None,
                        "detail": "Created"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not found!')

    def do_GET(self):
        if self.path == '/v1/blocks?limit=1&offset=0':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "data": [
                    {
                        "id": 159724,
                        "inserted_at": "2023-09-29T14:56:34.592463Z",
                        "height": 151533,
                        "txs": 1,
                        "hash": "36EE7A43201D0B20A60A730A352B55CD6BC73B815872F20DC8D881497439D9B5",  # noqa
                        "transactions": None
                    }
                ],
                "total_count": 151514,
                "error": False,
                "errors": None,
                "detail": "OK"
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == 'v1/tx_search/p':
            pass
        elif self.path == 'v1/broadcast':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"data":
                        {
                            "hash": "E08F7AD",
                            "code": 0,
                            "data": "",
                            "log": "",
                            "codespace": ""},
                        "total_count": 0,
                        "error": True,
                        "errors": None,
                        "detail": "Created"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Not found!')


class TestWebSocketClient(unittest.TestCase):
    HOST = 'localhost'
    PORT = 9000

    def start_dummy_http_server(self):
        server = HTTPServer((self.HOST, self.PORT), DummyHandler)
        t = threading.Thread(target=server.serve_forever, daemon=True)
        t.start()
        print('dummy http server is running.')

    def test_client(self):
        self.start_dummy_http_server()
        time.sleep(1)
        client = HttpClient(f"http://{self.HOST}:{self.PORT}")
        rsp = client.get_last_block()
        self.assertEqual(True, rsp.success)

        rsp = client.broadcast(
            tx_id=1, version=1, fee=0, data="", sign="", tx_type="",
            sender_address="from", recipient_address="to")
        self.assertEqual(True, rsp.success)


if __name__ == '__main__':
    unittest.main()
