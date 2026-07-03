from unittest.mock import Mock, patch

import websocket

from steam.client import SteamClient
from steam.core.cm import CMClient
from steam.core.connection import WebSocketConnection


def test_websocket_connection_sends_raw_binary_without_tcp_framing():
    connection = WebSocketConnection()
    connection.socket = Mock()
    connection.send_queue.put(b'raw-steam-message')

    connection._writer_loop_once()

    connection.socket.send_binary.assert_called_once_with(b'raw-steam-message')


def test_websocket_connection_put_message_sends_immediately():
    connection = WebSocketConnection()
    connection.socket = Mock()

    connection.put_message(b'raw-steam-message')

    connection.socket.send_binary.assert_called_once_with(b'raw-steam-message')


def test_websocket_connection_receives_raw_binary_without_tcp_framing():
    connection = WebSocketConnection()
    connection.socket = Mock(recv=Mock(return_value=b'raw-steam-message'))

    connection._reader_loop_once()

    assert connection.recv_queue.get_nowait() == b'raw-steam-message'


def test_websocket_connection_reader_timeout_keeps_connection_open():
    connection = WebSocketConnection()
    connection.socket = Mock(recv=Mock(side_effect=websocket.WebSocketTimeoutException))
    connection.disconnect = Mock()

    connection._reader_loop_once()

    connection.disconnect.assert_not_called()


def test_cm_client_marks_websocket_connection_as_channel_secured_on_connect():
    client = SteamClient(protocol=CMClient.PROTOCOL_WEBSOCKET)
    client.cm_servers.merge_list(['cm.example.com:443'])

    with patch.object(client.connection, 'connect', return_value=True), patch('gevent.spawn'):
        assert client.connect(retry=1) is True

    assert client.channel_secured is True
