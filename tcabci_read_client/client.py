import json
import logging
import threading
from collections import namedtuple
from urllib.parse import urljoin
from enum import Enum
import requests
import websocket


VERSION = 'v0.1.6'

logger = logging.getLogger('tcabci-read-client')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - '
    '%(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)


class MessageType(Enum):
    SUBSCRIBE = 'subscribe'
    UNSUBSCRIBE = 'unsubscribe'


HttpResultTuple = namedtuple(
    'HttpResultTuple', 'success error_message result')


class HttpClient:

    def __init__(self, http_url, http_headers=None):
        self.http_url = http_url
        if http_headers is None:
            http_headers = {
                'Client': f'tcabaci-read-python-client-{VERSION}'
            }
        self.http_headers = http_headers

    def get_last_block(self):
        url = urljoin(self.http_url, 'v1/blocks?limit=1&offset=0')
        req = requests.get(url, headers=self.http_headers)
        if not req.ok:
            return HttpResultTuple(
                success=False,
                error_message='invalid status code', result=req.content)
        try:
            response = req.json()
        except Exception as e:
            logger.error(e)
            return HttpResultTuple(
                success=False, error_message=str(e), result=req.content)

        result = {"blocks": response["data"],
                  "total_count": response["total_count"]}
        return HttpResultTuple(
            success=True, error_message=None, result=result)

    def broadcast(self, tx_id, version, fee, data, sign, tx_type,
                  sender_address, recipient_address):
        transaction = {
            "fee": fee,
            "id": tx_id,
            "version": version,
            "data": data,
            "sign": sign,
            "type": tx_type,
            "sender_addr": sender_address,
            "recipient_addr": recipient_address
        }
        payload = json.dumps(transaction)
        url = urljoin(self.http_url, 'v1/broadcast')
        req = requests.post(url, data=payload, headers=self.http_headers)
        if not req.ok:
            logger.error("invalid status code")
            return HttpResultTuple(
                success=False, error_message='invalid status code',
                result=req.content)
        try:
            response = req.json()
        except Exception as e:
            logger.error(e)
            return HttpResultTuple(
                success=False, error_message=str(e), result=req.content)
        return HttpResultTuple(
            success=True, error_message=None, result=response)

    def tx_search(self, *args, **kwargs):
        pre_payload = {
            "recipient_addrs": kwargs.get('recipient_addrs'),
            "sender_addrs": kwargs.get('sender_addrs'),
            "hashes": kwargs.get('hashes'),
            "typ": kwargs.get('typ'),
            "limit": kwargs.get('limit'),
            "offset": kwargs.get('offset'),
            "order_field": kwargs.get('order_field'),
            "order_by": kwargs.get('order_by')
        }
        height_operator = kwargs.get('height_operator')
        height = kwargs.get('height')
        if height_operator and height is not None:
            pre_payload['height'] = f"{height_operator} {height}"

        payload = {k: v for k, v in pre_payload.items() if v is not None}
        url = urljoin(self.http_url, 'v1/tx_search/p')
        req = requests.post(url, json=payload, headers=self.http_headers)
        if req.status_code == 400:
            logger.error('invalid arguments')
            return HttpResultTuple(
                success=False, error_message='invalid arguments',
                result=req.content)

        if not req.ok:
            logger.error("invalid status code")
            return HttpResultTuple(
                success=False, error_message='invalid status code',
                result=req.content)

        try:
            response = req.json()
        except Exception as e:
            logger.error(e)
            return HttpResultTuple(
                success=False, error_message=str(e), result=req.content)

        result = {"txs": response["data"],
                  "total_count": response["total_count"]}
        return HttpResultTuple(
            success=True, error_message=None, result=result)


class WsClient(object):

    def __init__(self, ws_url, message_callback, error_callback):
        self.ws_url = ws_url
        self.message_callback = message_callback
        self.error_callback = error_callback

        self.__listen = None
        self.websocket = None
        self.subscribed_addresses = set()

    def listener(self):
        logger.debug('Websocket listener is starting')
        while self.__listen is None:
            try:
                message = self.websocket.recv()
                self.message_callback(message)
            except Exception as e:
                self.error_callback(e)

    def ws(self):
        self.websocket = websocket.create_connection(self.ws_url)
        logger.debug("WebSocket connection opened")

    def start(self):
        logger.debug("Websocket client starting")
        self.ws()
        thd = threading.Thread(target=self.listener, daemon=True)
        thd.start()

    def stop(self):
        self.websocket.close()
        self.websocket = None
        self.__listen = False
        self.subscribed_addresses = set()
        logger.debug("WebSocket connection closed")

    def subscribe(self, address):
        address = set(address) - self.subscribed_addresses
        payload = json.dumps({
            "IsWeb": True,
            "Type": MessageType.SUBSCRIBE.value,
            "Addrs": list(address)
        })

        self.websocket.send(payload)
        self.subscribed_addresses.update(address)

    def unsubscribe(self, address=None):
        if not address:
            address = self.subscribed_addresses
        address = set(address)
        self.subscribed_addresses = self.subscribed_addresses - address
        payload = json.dumps({
            "IsWeb": True,
            "Type": MessageType.UNSUBSCRIBE.value,
            "Addrs": list(address)
        })
        self.websocket.send(payload)

    def get_subscribe_addresses(self):
        return self.subscribed_addresses
