import requests
import json
import asyncio
from Exceptions import AccessTokenExpired, TorBoxException
from Apis import Store
from typing import Optional, Tuple, TypeVar, Generic, Dict, Any, List
import aiohttp

T = TypeVar('T')


class TorBoxRequests:
    def __init__(self, http_client: requests.Session, store: Store):
        self._http_client = http_client
        self._store = store

    async def request(self, base_url: str,
                      url: str,
                      header_output: Optional[str],
                      require_authentication: bool,
                      request_type: 'RequestType',
                      data: Optional[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
        self._http_client.headers.pop("Authorization", None)

        if require_authentication:
            self._http_client.headers["Authorization"] = f"Bearer {self._store.bearer_token}"

        retry_count = 0
        while True:
            try:
                if request_type == RequestType.Get:
                    response = self._http_client.get(f"{base_url}{url}")
                elif request_type == RequestType.Post:
                    response = self._http_client.post(
                        f"{base_url}{url}", data=data)
                else:
                    raise ValueError("Invalid request type")

                text = response.content.decode('utf-8')

                if response.status_code == 401 and require_authentication and self._store.authentication_type == 'OAuth2':
                    tor_box_exception = self.parse_tor_box_exception(text)

                    if tor_box_exception and tor_box_exception.error == "BAD_TOKEN":
                        raise AccessTokenExpired()

                if response.status_code == 204:
                    text = None

                if not response.ok:
                    tor_box_exception = self.parse_tor_box_exception(text)

                    if tor_box_exception:
                        raise tor_box_exception
                    else:
                        raise Exception(text)

                if header_output:
                    header_value = response.headers.get(header_output)
                    return text, header_value

                return text, None
            except TorBoxException:
                raise
            except Exception:
                if retry_count >= self._store.retry_count:
                    raise

                retry_count += 1
                await asyncio.sleep(1 * retry_count)

    async def request_generic(self, base_url: str,
                              url: str,
                              require_authentication: bool,
                              request_type: 'RequestType',
                              data: Optional[Dict[str, Any]]) -> T:
        result, _ = await self.request(base_url, url, None, require_authentication, request_type, data)

        if result is None:
            return T()

        try:
            return json.loads(result)
        except json.JSONDecodeError as ex:
            raise json.JSONDecodeError(
                f"Unable to deserialize response. Response was: {result}", ex)
        except Exception as ex:
            raise Exception(
                f"Unable to deserialize response. Response was: {result}", ex)

    async def get_auth_request_async(self, url: str) -> T:
        return await self.request_generic(self._store.auth_url, url, False, RequestType.Get, None)

    async def post_auth_request_async(self, url: str, data: List[Tuple[str, Optional[str]]]) -> T:
        content = {k: v for k, v in data}
        return await self.request_generic(self._store.auth_url, url, False, RequestType.Post, content)

    async def get_request_header_async(self, url: str, header: str, require_authentication: bool) -> Optional[str]:
        _, header_value = await self.request(self._store.api_url, url, header, require_authentication, RequestType.Get, None)
        return header_value

    async def get_request_async(self, url: str, require_authentication: bool) -> Optional[str]:
        text, _ = await self.request(self._store.api_url, url, None, require_authentication, RequestType.Get, None)
        return text

    async def get_request_async_generic(self, url: str, require_authentication: bool) -> T:
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Get, None)

    async def get_link_request_async(self, url: str, require_authentication: bool) -> T:
        url += f"&token={self._store.bearer_token}"
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Get, None)

    async def post_request_async(self, url: str, data: Optional[List[Tuple[str, Optional[str]]]], require_authentication: bool):
        await self.request(self._store.api_url, url, None, require_authentication, RequestType.Post, data)

    async def post_request_raw_async(self, url: str, data: Optional[Dict[str, Any]], require_authentication: bool):
        await self.request(self._store.api_url, url, None, require_authentication, RequestType.Post, data)

    async def post_request_raw_async_generic(self, url: str, data: Optional[Dict[str, Any]], require_authentication: bool) -> T:
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Post, data)

    async def post_request_async_generic(self, url: str, data: Optional[List[Tuple[str, Optional[str]]]], require_authentication: bool) -> T:
        # content = {k: v for k, v in data} if data else None
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Post, data)

    async def post_request_multipart_async(self, url: str, data: Optional[Dict[str, Any]], require_authentication: bool) -> T:
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Post, data)

    async def put_request_async(self, url: str, file: bytes, require_authentication: bool):
        content = file
        await self.request(self._store.api_url, url, None, require_authentication, RequestType.Put, content)

    async def put_request_async_generic(self, url: str, file: bytes, require_authentication: bool) -> T:
        content = file
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Put, content)

    async def delete_request_async(self, url: str, require_authentication: bool):
        await self.request(self._store.api_url, url, None, require_authentication, RequestType.Delete, None)

    @staticmethod
    def parse_tor_box_exception(text: Optional[str]) -> Optional['TorBoxException']:
        try:
            if text is None:
                return None

            request_error = json.loads(text)

            if 'error' in request_error:
                return TorBoxException(request_error['error'], request_error.get('detail'))

            return None
        except Exception:
            return None


class RequestType:
    Get = 'GET'
    Post = 'POST'
    Put = 'PUT'
    Delete = 'DELETE'
