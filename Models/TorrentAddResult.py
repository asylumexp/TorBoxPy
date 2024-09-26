from pydantic import BaseModel
from typing import Optional

class TorrentAddResult(BaseModel):
    """Represents the result of adding a torrent."""
    
    hash: Optional[str] = None  # Torrent hash
    torrent_id: Optional[int] = None  # Torrent ID
    auth_id: Optional[str] = None  # Auth ID
