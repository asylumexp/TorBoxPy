from enum import Enum


class AuthenticationType(Enum):
    Api = 1
    OAuth2 = 2


class Store:
    def __init__(self):
        self.auth_url = "https://api.real-debrid.com/oauth/v2/"
        self.api_url = "https://api.torbox.app/v1/api/"
        self.app_id = int
        self.retry_count = 0
        self.authentication_type = None
        self.api_key = None
        self.device_code = None
        self.oauth_access_token = None
        self.oauth_client_id = None
        self.oauth_client_secret = None
        self.oauth_refresh_token = None

    @property
    def bearer_token(self):
        if self.authentication_type == AuthenticationType.Api:
            if not self.api_key or not self.api_key.strip():
                raise Exception(
                    "No API key set, make sure to call UseApiAuthentication with a valid API key.")
            return self.api_key
        elif self.authentication_type == AuthenticationType.OAuth2:
            if not self.oauth_access_token or not self.oauth_access_token.strip():
                raise Exception(
                    "No access token set, make sure to call UseOAuthFlowAuthentication with a valid access token.")
            return self.oauth_access_token
        else:
            raise Exception("No valid authentication token found.")
