from unittest.mock import Mock

from steam.webauth import WebAuth


def test_webauth_can_start_credentials_session_for_steam_client_platform():
    auth = WebAuth(
        'account-name',
        'password',
        platform_type=1,
        website_id='Client',
        device_friendly_name='DESKTOP-test',
    )
    auth.send_api_request = Mock(
        return_value={
            'response': {
                'client_id': '123',
                'request_id': 'request-id',
                'steamid': '76561198000000000',
                'allowed_confirmations': [],
            }
        }
    )

    auth._start_session_with_credentials('encrypted-password', 42)

    data = auth.send_api_request.call_args.kwargs['data']
    assert data['platform_type'] == '1'
    assert data['website_id'] == 'Client'
    assert data['device_friendly_name'] == 'DESKTOP-test'
