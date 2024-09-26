from typing import List, Optional
from pydantic import BaseModel

class AvailableTorrentFile(BaseModel):
    """Represents a file within a torrent."""
    
    name: str  # File name
    size: int  # File size

class AvailableTorrent(BaseModel):
    """Represents an available torrent."""
    
    name: str  # Torrent name
    size: int  # Torrent size in bytes
    hash: str  # Torrent hash
    files: Optional[List[AvailableTorrentFile]] = None  # Torrent files
