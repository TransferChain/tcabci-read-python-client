# tcabci-read-python-client

It is used to listen to the read nodes of TransferChain and send requests to the Block Explorer.

## Installation

This client requires python>=3.8
```sh
pip install tcabci-read-client
```
```sh
pip install git+https://github.com/TransferChain/tcabci-read-python-client@main
```

## Constants
##### Read node websocket url
```sh
wss://read-node-01.transferchain.io/ws
```
##### Read node http url
```sh
https://read-node-01.transferchain.io
```
## Examples
##### read-node event listener and subscribe example
```python
from tcabci_read_client import WsClient
def message_callback(message):
    print(f"Received message: {message}")

def error_callback(error):
    print(f"Error: {error}")

client = WsClient("wss://read-node-01.transferchain.io/ws",
        message_callback=message_callback,
        error_callback=error_callback)
client.start()
client.subscribe(['addresses'])
client.unsubscribe(['addresses'])
client.get_subscribe_addresses()
```
##### Http client example
```python
from tcabci_read_client import HttpClient
client = HttpClient("https://read-node-01.transferchain.io")
client.get_last_block()
'''
client.tx_search params;
limit, order_field,offset,order_by,hashes,typ,sender_addrs,recipient_addrs
'''
client.tx_search(sender_addrs='test_address', recipient_addrs='test_address2')
client.broadcast(tx_id="", version=1, fee=0, data="", sign="", tx_type="", sender_address="from", recipient_address="to")

```

## License

MIT
