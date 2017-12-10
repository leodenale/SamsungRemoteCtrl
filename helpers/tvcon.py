import socket
import websocket
import samsungctl
import logging
import time

def send(config, key, wait_time=100.0):
    try:
        with samsungctl.Remote(config) as remote:
            remote.control(key)

        time.sleep(wait_time / 1000.0)
        return True

    except socket.error:
        return False
    except websocket._exceptions.WebSocketConnectionClosedException:
        logging.error('Websocket error! Maybe try sending with legacy (-l)?')
        return False
