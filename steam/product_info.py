from collections.abc import Callable, Sequence
from typing import Any

from steam.client import SteamClient
from steam.enums import EResult
from steam.webauth import WebAuth


class SteamProductInfoError(Exception):
    """Raised when Steam product info cannot be fetched."""


class SteamProductInfoClient:
    def __init__(
            self,
            username: str = '',
            password: str = '',
            refresh_token: str = '',
            steam_guard_code: str | None = None,
            timeout: int = 30,
            steam_client_factory: Callable[[], SteamClient] = SteamClient,
            web_auth_factory: Callable[..., WebAuth] = WebAuth,
    ):
        self.username = username
        self.password = password
        self.refresh_token = refresh_token
        self.steam_guard_code = steam_guard_code
        self.timeout = timeout
        self.steam_client_factory = steam_client_factory
        self.web_auth_factory = web_auth_factory

    def get_product_info(self, app_ids: Sequence[int]) -> dict[str, Any]:
        steam_client = self.steam_client_factory()
        try:
            refresh_token = self.refresh_token or self._get_refresh_token_from_credentials()
            login_result = steam_client.login_with_refresh_token(self.username, refresh_token)
            if login_result != EResult.OK:
                raise SteamProductInfoError(f'Steam login failed: {login_result!s}')

            return steam_client.get_product_info(
                apps=list(app_ids),
                packages=[],
                timeout=self.timeout,
            )
        finally:
            steam_client.logout()

    def _get_refresh_token_from_credentials(self) -> str:
        if not self.username or not self.password:
            raise SteamProductInfoError('Steam username/password or refresh token is required')

        web_auth = self.web_auth_factory(
            username=self.username,
            password=self.password,
            platform_type=1,
            website_id='Client',
            device_friendly_name='SteamProductInfoClient',
        )
        web_auth.login(self.username, self.password, self.steam_guard_code)

        if not web_auth.refresh_token:
            raise SteamProductInfoError('Steam authentication did not return refresh token')

        return web_auth.refresh_token
