from unittest.mock import Mock

from steam.enums import EResult
from steam.product_info import SteamProductInfoClient


def test_product_info_client_logs_in_with_refresh_token_and_fetches_product_info():
    steam_client = Mock()
    steam_client.login_with_refresh_token.return_value = EResult.OK
    steam_client.get_product_info.return_value = {'apps': {730: {'appid': 730}}, 'packages': {}}

    client = SteamProductInfoClient(
        username='account-name',
        refresh_token='refresh-token-value',
        steam_client_factory=lambda: steam_client,
    )

    result = client.get_product_info([730])

    assert result == {'apps': {730: {'appid': 730}}, 'packages': {}}
    steam_client.login_with_refresh_token.assert_called_once_with('account-name', 'refresh-token-value')
    steam_client.get_product_info.assert_called_once_with(apps=[730], packages=[], timeout=30)
    steam_client.logout.assert_called_once_with()


def test_product_info_client_gets_refresh_token_from_credentials_when_token_is_not_provided():
    steam_client = Mock()
    steam_client.login_with_refresh_token.return_value = EResult.OK
    steam_client.get_product_info.return_value = {'apps': {}, 'packages': {}}
    web_auth = Mock(refresh_token='generated-refresh-token')

    client = SteamProductInfoClient(
        username='account-name',
        password='password',
        steam_client_factory=lambda: steam_client,
        web_auth_factory=lambda **kwargs: web_auth,
    )

    client.get_product_info([570])

    web_auth.login.assert_called_once_with('account-name', 'password', None)
    steam_client.login_with_refresh_token.assert_called_once_with('account-name', 'generated-refresh-token')
