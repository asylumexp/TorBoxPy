import json
import http.client
from urllib.parse import urlencode
from typing import List, Optional
from Models import AvailableUsenet, Response, UsenetAddResult, UsenetInfoResult
from Apis import TorBoxRequests, Store


class UsenetApi:
    def __init__(self, http_client: http.client.HTTPConnection, store: Store):
        self._requests = TorBoxRequests(http_client, store)
        self._store = store

    async def get_current_async(self, skip_cache: bool = False) -> Optional[List[UsenetInfoResult]]:
        list_data = await self._requests.get_request_async(f"usenet/mylist?bypass_cache={skip_cache}", True)

        if list_data is None:
            return None

        return json.loads(list_data).get('data')

    async def get_hash_info_async(self, hash: str, skip_cache: bool = False) -> Optional[UsenetInfoResult]:
        current_downloads = await self.get_current_async(skip_cache)

        if current_downloads is None:
            return None

        return next((item for item in current_downloads if item.hash == hash), None)

    async def get_id_info_async(self, id: int, skip_cache: bool = False) -> Optional[UsenetInfoResult]:
        current_download = await self._requests.get_request_async(f"usenet/mylist?bypass_cache={skip_cache}", True)

        return current_download.get('data') if current_download else None

    async def add_file_async(self, file: bytes, post_processing: int = -1, name: Optional[str] = None, password: Optional[str] = None) -> Response[UsenetAddResult]:
        content = {
            'file': ('nzb.nzb', file, 'application/x-nzb'),
            'post_processing': str(post_processing),
            'name': name,
            'password': password
        }

        return await self._requests.post_request_multipart_async("usenet/createusenetdownload", content, True)

    async def add_link_async(self, link: str, post_processing: int = -1, name: Optional[str] = None, password: Optional[str] = None) -> Response[UsenetAddResult]:
        data = {
            'link': link,
            'post_processing': str(post_processing),
            'name': name,
            'password': password
        }

        return await self._requests.post_request_async("usenet/createusenetdownload", data, True)

    async def control_async(self, hash: str, action: str, all: bool = False) -> Response:
        info = await self.get_hash_info_async(hash, skip_cache=True)

        data = {
            'usenet_id': info.id if info else None,
            'operation': action,
            'all': all
        }

        json_content = json.dumps(data)
        return await self._requests.post_request_raw_async("usenet/controlusenetdownload", json_content, True)

    async def get_availability_async(self, hash: str, list_files: bool = False) -> Response[List[Optional[AvailableUsenet]]]:
        return await self._requests.get_request_async(f"usenet/checkcached?hash={hash}&format=list&list_files={list_files}", True)

    async def request_download_async(self, usenet_id: int, file_id: Optional[int], zip: bool = False) -> Response[str]:
        parameters = {
            'token': self._store.bearer_token,
            'usenet_id': str(usenet_id),
            'file_id': str(file_id) if file_id is not None else None,
            'zip': str(zip)
        }

        uri = f"usenet/requestdl?{urlencode(parameters)}"
        return await self._requests.get_request_async(uri, True)
