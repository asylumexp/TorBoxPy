from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class QueuedTorrent(BaseModel):
    """Represents a queued torrent."""
    
    id: int  # Torrent ID
    auth_id: str  # Auth ID
    created_at: datetime  # Creation date and time
    magnet: str  # Magnet link
    torrent_file: Optional[str] = None  # Torrent file (optional)
    hash: str  # Torrent hash
    name: str  # Torrent name
    type: str  # Torrent type
