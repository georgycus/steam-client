import base64
import json
from unittest.mock import Mock

from steam.client import SteamClient
from steam.enums import EResult


class LogonResponse:
    def __init__(self, eresult: EResult):
        self.body = Mock(eresult=eresult)


def make_refresh_token(steam_id: int) -> str:
    payload = base64.urlsafe_b64encode(json.dumps({'sub': str(steam_id)}).encode()).decode().rstrip('=')
    return f'header.{payload}.signature'


def test_login_with_refresh_token_sends_token_as_client_logon_access_token():
    steam_id = 76561199656228249
    refresh_token = make_refresh_token(steam_id)
    client = SteamClient()
    client.connection = Mock(local_address='127.0.0.1')
    client._pre_login = Mock(return_value=EResult.OK)
    client.send = Mock()
    client.wait_msg = Mock(return_value=LogonResponse(EResult.OK))
    client.sleep = Mock()

    result = client.login_with_refresh_token('account-name', refresh_token)

    assert result == EResult.OK
    client.send.assert_called_once()
    message = client.send.call_args.args[0]
    assert message.header.steamid == steam_id
    assert message.body.account_name == ''
    assert message.body.access_token == refresh_token
    assert message.body.password == ''
    assert message.body.login_key == ''
    assert message.body.obfuscated_private_ip.v4 == 0
    assert message.body.machine_name.startswith('DESKTOP-')
