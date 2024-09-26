import pytest
from Exceptions import TorBoxException
from TorBox import TorBoxPyClient
from pathlib import Path


def get_api_key():
    with open("secret.txt") as f:
        return f.read().strip()


@pytest.fixture
def client():
    client = TorBoxPyClient()
    client.use_api_authentication(get_api_key())
    return client


@pytest.mark.asyncio
async def test_current_torrents(client: TorBoxPyClient):
    result = await client.torrents.get_current_async(True)
    assert result is not None


@pytest.mark.asyncio
async def test_queued_torrents(client: TorBoxPyClient):
    result = await client.torrents.get_queued_async(True)
    assert result is not None


@pytest.mark.asyncio
async def test_info(client: TorBoxPyClient):
    result = await client.torrents.get_hash_info_async("dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c")
    assert result is not None


@pytest.mark.asyncio
async def test_add_file(client: TorBoxPyClient):
    file_path = Path("big-buck-bunny.torrent")
    file_bytes = file_path.read_bytes()

    result = await client.torrents.add_file_async(file_bytes, 1, False, "Big Buck Bunny")
    assert result['success']  # Adjust based on actual response structure


@pytest.mark.asyncio
async def test_add_magnet(client: TorBoxPyClient):
    magnet_link = "magnet:?xt=urn:btih:dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c&dn=Big+Buck+Bunny&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969"
    result = await client.torrents.add_magnet_async(magnet_link)
    assert result['success']  # Adjust based on actual response structure


@pytest.mark.asyncio
async def test_control_torrent(client: TorBoxPyClient):
    hash = "dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c"
    action = "pause"
    with pytest.raises(TorBoxException):
        result = await client.torrents.control_async(hash, action)
        assert result is not None  # Adjust based on actual response structure


@pytest.mark.asyncio
async def test_check_availability(client: TorBoxPyClient):
    hash = "dd8255ecdc7ca55fb0bbf81323d87062db1f6d1c"
    result = await client.torrents.get_availability_async(hash, False)
    assert result  # Adjust based on actual response structure


@pytest.mark.asyncio
async def test_request_download(client: TorBoxPyClient):
    torrent_id = 123
    file_id = 456

    with pytest.raises(TorBoxException):
        await client.torrents.request_download_async(torrent_id, file_id, False)
