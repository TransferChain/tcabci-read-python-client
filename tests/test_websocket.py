import unittest
import json
import time
import asyncio
import threading
import websockets
from tcabci_read_client import WsClient


def simple_ws_server(host, port, loop):
    asyncio.set_event_loop(loop)

    async def echo(websocket, path):
        async for message in websocket:
            await websocket.send(message)

    start_server = websockets.serve(echo, host, port)
    try:
        loop.run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except OSError:
        pass


class TestWebSocketClient(unittest.TestCase):

    def test_client(self):
        host = 'localhost'
        port = 8000
        loop = asyncio.new_event_loop()
        t = threading.Thread(target=simple_ws_server,
                             args=(host, port, loop),
                             daemon=True)
        t.start()
        time.sleep(1)

        def message_callback(message):
            if not message:
                return
            message_json = json.loads(message)
            self.assertEqual(message_json['Addrs'][0], 'test')

        def error_callback(error):
            pass

        ws_client = WsClient(
            f"ws://{host}:{port}/ws",
            message_callback=message_callback,
            error_callback=error_callback)
        ws_client.start()
        ws_client.subscribe(['test'])
        ws_client.unsubscribe(['test'])
        time.sleep(1)
        ws_client.stop()


if __name__ == '__main__':
    unittest.main()
