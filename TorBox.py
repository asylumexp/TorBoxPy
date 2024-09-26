import requests
from Apis import TorrentsApi, Store, AuthenticationType


class TorBoxPyClient:
    """
    The TorBoxNetClient consumes the Real-Debrid.com API.
    Documentation about the API can be found here: https://api.real-debrid.com/
    """

    def __init__(self, app_id=None, http_client=None, retry_count=1):
        """
        Initialize the TorBoxNet API.
        To use authentication make sure to call either use_api_authentication for Api Key authentication
        or use_oauth_authentication for Auth2 authentication. The latter is also used for Device authentication.

        :param app_id: The ID of your application. If None the app id will be set to the default Opensource App ID
                       X245A4XAIBGVM. You can request a new key through the Help section on Real-Debrid.
        :param http_client: Optional requests.Session if you want to use your own Session.
        :param retry_count: The API will retry this many times before failing.
        """
        self._store = Store()
        self._store.app_id = app_id or "X245A4XAIBGVM"
        self._store.retry_count = retry_count

        self.client = http_client or requests.Session()

        self.torrents = TorrentsApi(self.client, self._store)
        # self.usenet = UsenetApi(self.client, self._store)
        # self.user = UserApi(self.client, self._store)

    def use_api_authentication(self, api_key):
        """
        Initialize the API to use ApiToken authentication. The token must be manually retrieved from
        https://real-debrid.com/apitoken and stored in your application.

        :param api_key: The API for the user, retrieved from https://real-debrid.com/apitoken.
        """
        if not api_key or api_key.strip() == "":
            raise ValueError("Api Key cannot be null")

        self._store.authentication_type = AuthenticationType.Api
        self._store.api_key = api_key

    def use_oauth_authentication(self, client_id=None, client_secret=None, access_token=None, refresh_token=None):
        """
        Initialize the API to use three legged OAuth2 authentication.
        This method should also be used for device authentication.
        To see the flow use https://api.real-debrid.com/#device_auth as a reference.
        To use call the following methods:
        - oauth_authorization_url
        - oauth_authorization_response_async
        When receiving the authentication tokens, save the "access_token" and "refresh_token" in your database for future for each user.

        To use device authentication use the following methods first:
        - get_device_code
        - device_auth_verify_async. Poll this method every 5 seconds.
        - oauth_authorization_response_async. Use this to trade the device code for an access token.
        When receiving the authentication tokens, save the "client_id", "client_secret", "access_token" and "refresh_token" in your database for future for each user.

        :param client_id: The client_id for your application or received client_id from token authentication.
        :param client_secret: The client_secret for your application or received client_id from token authentication.
        :param access_token: The access_token from previously authenticated user.
        :param refresh_token: The refresh_token from previously authenticated user.
        """
        self._store.authentication_type = AuthenticationType.OAuth2
        self._store.oauth_client_id = client_id
        self._store.oauth_client_secret = client_secret
        self._store.oauth_access_token = access_token
        self._store.oauth_refresh_token = refresh_token
