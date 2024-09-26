import pytest
from Exceptions import TorBoxException
from TorBox import TorBoxPyClient
from pathlib import Path


def get_api_key():
    with open("secret.txt") as f:
        return f.read().strip()


@pytest.fixture
async def client():
    client = TorBoxPyClient()
    client.use_api_authentication(get_api_key())
    return client


@pytest.mark.asyncio
async def test_current_usenet_downloads(client):
    result = await client.usenet.get_current_async(True)
    assert result is not None


@pytest.mark.asyncio
async def test_hash_info(client):
    result = await client.usenet.get_hash_info_async("1c414b53446c0249abfc2bb705e42ffe")
    assert result is not None


@pytest.mark.asyncio
async def test_add_usenet_file(client):
    file_path = Path("big-buck-bunny.nzb")
    file_bytes = await file_path.read_bytes()

    result = await client.usenet.add_file_async(file_bytes, 3, "Big Buck Bunny")
    assert result['success']  # Adjust based on actual response structure


@pytest.mark.asyncio
async def test_add_usenet_link(client):
    link = "https://gist.github.com/sanderjo/aa1f9d4720696cc11640/raw/dd9a3e14df80353f2ad187cc5cd5f5dafe9f2d24/Big.Buck.Bunny%2520---%2520missing%2520segemnts.nzb"
    result = await client.usenet.add_link_async(link)
    assert result['success']  # Adjust based on actual response structure


@pytest.mark.asyncio
async def test_control_usenet(client):
    hash = "1c414b53446c0249abfc2bb705e42ffe"
    action = "delete"

    result = await client.usenet.control_async(hash, action)
    assert result['success']  # Adjust based on actual response structure


@pytest.mark.asyncio
async def test_usenet_availability(client):
    hash = "1c414b53446c0249abfc2bb705e42ffe"
    result = await client.usenet.get_availability_async(hash, False)
    assert result['success']  # Adjust based on actual response structure


@pytest.mark.asyncio
async def test_usenet_request_download(client):
    usenet_id = 123
    file_id = 456

    with pytest.raises(TorBoxException):
        await client.usenet.request_download_async(usenet_id, file_id, False)
