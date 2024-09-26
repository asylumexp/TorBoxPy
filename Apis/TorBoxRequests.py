import requests
import json
import asyncio
from Exceptions import AccessTokenExpired, TorBoxException
from Apis import Store
from typing import Optional, Tuple, TypeVar, Generic, Dict, Any, List

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
                      data: Optional[Dict[str, Any]],
                      cancellation_token: Any) -> Tuple[Optional[str], Optional[str]]:
        self._http_client.headers.pop("Authorization", None)

        if require_authentication:
            self._http_client.headers["Authorization"] = f"Bearer {self._store.bearer_token}"

        retry_count = 0
        while True:
            try:
                if request_type == RequestType.Get:
                    response = self._http_client.get(
                        f"{base_url}{url}", timeout=cancellation_token)
                elif request_type == RequestType.Post:
                    response = self._http_client.post(
                        f"{base_url}{url}", data=data, timeout=cancellation_token)
                elif request_type == RequestType.Put:
                    response = self._http_client.put(
                        f"{base_url}{url}", data=data, timeout=cancellation_token)
                elif request_type == RequestType.Delete:
                    response = self._http_client.delete(
                        f"{base_url}{url}", timeout=cancellation_token)
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
                              data: Optional[Dict[str, Any]],
                              cancellation_token: Any) -> T:
        result, _ = await self.request(base_url, url, None, require_authentication, request_type, data, cancellation_token)

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

    async def get_auth_request_async(self, url: str, cancellation_token: Any) -> T:
        return await self.request_generic(self._store.auth_url, url, False, RequestType.Get, None, cancellation_token)

    async def post_auth_request_async(self, url: str, data: List[Tuple[str, Optional[str]]], cancellation_token: Any) -> T:
        content = {k: v for k, v in data}
        return await self.request_generic(self._store.auth_url, url, False, RequestType.Post, content, cancellation_token)

    async def get_request_header_async(self, url: str, header: str, require_authentication: bool, cancellation_token: Any) -> Optional[str]:
        _, header_value = await self.request(self._store.api_url, url, header, require_authentication, RequestType.Get, None, cancellation_token)
        return header_value

    async def get_request_async(self, url: str, require_authentication: bool, cancellation_token: Any) -> Optional[str]:
        text, _ = await self.request(self._store.api_url, url, None, require_authentication, RequestType.Get, None, cancellation_token)
        return text

    async def get_request_async_generic(self, url: str, require_authentication: bool, cancellation_token: Any) -> T:
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Get, None, cancellation_token)

    async def get_link_request_async(self, url: str, require_authentication: bool, cancellation_token: Any) -> T:
        url += f"&token={self._store.bearer_token}"
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Get, None, cancellation_token)

    async def post_request_async(self, url: str, data: Optional[List[Tuple[str, Optional[str]]]], require_authentication: bool, cancellation_token: Any):
        content = {k: v for k, v in data} if data else None
        await self.request(self._store.api_url, url, None, require_authentication, RequestType.Post, content, cancellation_token)

    async def post_request_raw_async(self, url: str, data: Optional[Dict[str, Any]], require_authentication: bool, cancellation_token: Any):
        await self.request(self._store.api_url, url, None, require_authentication, RequestType.Post, data, cancellation_token)

    async def post_request_raw_async_generic(self, url: str, data: Optional[Dict[str, Any]], require_authentication: bool, cancellation_token: Any) -> T:
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Post, data, cancellation_token)

    async def post_request_async_generic(self, url: str, data: Optional[List[Tuple[str, Optional[str]]]], require_authentication: bool, cancellation_token: Any) -> T:
        content = {k: v for k, v in data} if data else None
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Post, content, cancellation_token)

    async def post_request_multipart_async(self, url: str, data: Optional[Dict[str, Any]], require_authentication: bool, cancellation_token: Any) -> T:
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Post, data, cancellation_token)

    async def put_request_async(self, url: str, file: bytes, require_authentication: bool, cancellation_token: Any):
        content = file
        await self.request(self._store.api_url, url, None, require_authentication, RequestType.Put, content, cancellation_token)

    async def put_request_async_generic(self, url: str, file: bytes, require_authentication: bool, cancellation_token: Any) -> T:
        content = file
        return await self.request_generic(self._store.api_url, url, require_authentication, RequestType.Put, content, cancellation_token)

    async def delete_request_async(self, url: str, require_authentication: bool, cancellation_token: Any):
        await self.request(self._store.api_url, url, None, require_authentication, RequestType.Delete, None, cancellation_token)

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
