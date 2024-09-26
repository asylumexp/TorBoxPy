import json
import requests
from Apis import TorBoxRequests, Store
from typing import List, Optional, Dict, Any
from Models import AvailableTorrent, QueuedTorrent, Response, TorrentAddResult, TorrentInfoResult
class TorrentsApi:
    def __init__(self, http_client: requests.Session, store: 'Store'):
        self._requests = TorBoxRequests(http_client, store)
        self._store = store

    async def get_total(self, skip_cache: bool = False, cancellation_token: Optional[Any] = None) -> int:
        res = await self.get_current_async(skip_cache, cancellation_token)
        return -1 if res is None else len(res)

    async def get_current_async(self, skip_cache: bool = False, cancellation_token: Optional[Any] = None) -> Optional[List['TorrentInfoResult']]:
        list_response = await self._requests.get_request_async(f"torrents/mylist?bypass_cache={skip_cache}", True, cancellation_token)
        if list_response is None:
            return None
        return json.loads(list_response).get('data')

    async def get_queued_async(self, skip_cache: bool = False, cancellation_token: Optional[Any] = None) -> Optional[List['TorrentInfoResult']]:
        list_response = await self._requests.get_request_async("torrents/getqueued", True, cancellation_token)
        if list_response is None:
            return None
        queued_torrents = json.loads(list_response).get('data')
        torrents = [
            {
                'id': torrent['id'],
                'auth_id': torrent['auth_id'],
                'hash': torrent['hash'],
                'name': torrent['name'],
                'magnet': torrent['magnet'],
                'created_at': torrent['created_at'],
                'download_state': 'queued',
                'torrent_file': torrent['torrent_file'] is not None,
                'progress': 0.0,
                'files': [],
                'download_speed': 0,
                'seeds': 0,
                'updated_at': torrent['created_at']
            } for torrent in queued_torrents
        ]
        return torrents

    async def get_id_info_async(self, id: int, skip_cache: bool = False, cancellation_token: Optional[Any] = None) -> Optional['TorrentInfoResult']:
        current_torrent = await self._requests.get_request_async(f"torrents/mylist?bypass_cache={skip_cache}", True, cancellation_token)
        if current_torrent:
            torrent = json.loads(current_torrent).get('data')
            if torrent:
                return torrent
        queued_torrents = await self.get_queued_async(skip_cache, cancellation_token)
        if queued_torrents:
            for torrent in queued_torrents:
                if torrent['id'] == id:
                    return torrent
        return None

    async def get_hash_info_async(self, hash: str, skip_cache: bool = False, cancellation_token: Optional[Any] = None) -> Optional['TorrentInfoResult']:
        current_torrents = await self.get_current_async(skip_cache, cancellation_token)
        if current_torrents:
            for torrent in current_torrents:
                if torrent['hash'] == hash:
                    return torrent
        queued_torrents = await self.get_queued_async(skip_cache, cancellation_token)
        if queued_torrents:
            for torrent in queued_torrents:
                if torrent['hash'] == hash:
                    return torrent
        return None

    async def add_file_async(self, file: bytes, seeding: int = 1, allow_zip: bool = False, name: Optional[str] = None, cancellation_token: Optional[Any] = None) -> 'Response[TorrentAddResult]':
        content = {
            'file': ('torrent.torrent', file, 'application/x-bittorrent'),
            'seed': str(seeding),
            'allow_zip': str(allow_zip),
            'name': name
        }
        return await self._requests.post_request_multipart_async("torrents/createtorrent", content, True, cancellation_token)

    async def add_magnet_async(self, magnet: str, seeding: int = 1, allow_zip: bool = False, name: Optional[str] = None, cancellation_token: Optional[Any] = None) -> 'Response[TorrentAddResult]':
        data = {
            'magnet': magnet,
            'seed': str(seeding),
            'allow_zip': str(allow_zip),
            'name': name
        }
        return await self._requests.post_request_async("torrents/createtorrent", data, True, cancellation_token)

    async def control_async(self, hash: str, action: str, cancellation_token: Optional[Any] = None) -> 'Response':
        info = await self.get_hash_info_async(hash, skip_cache=True, cancellation_token=cancellation_token)
        data = {
            'torrent_id': info['id'],
            'operation': action
        }
        json_content = json.dumps(data)
        endpoint = "torrents/controlqueued" if info['download_state'] == "queued" else "torrents/controltorrent"
        return await self._requests.post_request_raw_async(endpoint, json_content, True, cancellation_token)

    async def get_availability_async(self, hash: str, list_files: bool = False, cancellation_token: Optional[Any] = None) -> 'Response[List[AvailableTorrent]]':
        return await self._requests.get_request_async(f"torrents/checkcached?hash={hash}&format=list&list_files={list_files}", True, cancellation_token)

    async def request_download_async(self, torrent_id: int, file_id: Optional[int], zip: bool = False, cancellation_token: Optional[Any] = None) -> 'Response[str]':
        parameters = {
            'token': self._store.bearer_token,
            'torrent_id': str(torrent_id),
            'file_id': str(file_id) if file_id is not None else None,
            'zip_link': str(zip)
        }
        return await self._requests.get_request_async(f"torrents/requestdl?{parameters}", True, cancellation_token)

