from unittest.mock import Mock

from steam.client import SteamClient
from steam.enums import EResult


class LogonResponse:
    def __init__(self, eresult: EResult):
        self.body = Mock(eresult=eresult)


def test_login_with_refresh_token_sends_token_as_client_logon_access_token():
    client = SteamClient()
    client.connection = Mock(local_address='127.0.0.1')
    client._pre_login = Mock(return_value=EResult.OK)
    client.send = Mock()
    client.wait_msg = Mock(return_value=LogonResponse(EResult.OK))
    client.sleep = Mock()

    result = client.login_with_refresh_token('account-name', 'refresh-token-value')

    assert result == EResult.OK
    client.send.assert_called_once()
    message = client.send.call_args.args[0]
    assert message.body.account_name == 'account-name'
    assert message.body.access_token == 'refresh-token-value'
    assert message.body.password == ''
    assert message.body.login_key == ''
